import logging
from contextlib import asynccontextmanager
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from hispanie.config import Config, Database
from hispanie.errors import DBError

ROOT = Path(__file__).parents[1].resolve()
ALEMBIC_PATH = ROOT.joinpath("alembic")

logger = logging.getLogger(__name__)

async_session_factory: async_sessionmaker[AsyncSession] | None = None


def _get_async_url(db: Database, suffix: str | None = None) -> str:
    url = f"postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}"
    if suffix:
        url += suffix
    return url


def _get_sync_url(db: Database, suffix: str | None = None) -> str:
    url = f"postgresql+psycopg://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}"
    if suffix:
        url += suffix
    return url


async def init() -> async_sessionmaker[AsyncSession]:
    global async_session_factory
    logger.info("Initialising async database session")
    engine = create_async_engine(_get_async_url(Config.database), echo=False)
    async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    return async_session_factory


async def close() -> None:
    global async_session_factory
    if async_session_factory:
        await async_session_factory().get_bind().dispose()
        async_session_factory = None


def get_alembic_config(conn):
    config = AlembicConfig()
    config.attributes["connection"] = conn
    config.set_section_option("alembic", "script_location", str(ALEMBIC_PATH))
    script = ScriptDirectory.from_config(config)
    context = MigrationContext.configure(conn)
    script_head = script.get_current_head()
    current_head = context.get_current_revision()

    return config, script, context, script_head, current_head


def get_missing_revisions(conn):
    _, script, _, script_head, current_head = get_alembic_config(conn)
    return [s for s in script.iterate_revisions(script_head, current_head)]


def _create_tables(conn, table_name: str, force: bool) -> bool:
    exists = True
    try:
        conn.execute(text(f"select 1 from {table_name} limit 1"))
    except Exception:
        exists = False

    if not exists or force:
        from .model import Base

        logger.info("Creating all tables %s", list(Base.metadata.tables))
        Base.metadata.create_all(bind=conn)

    return exists


def _apply_migrations(conn, exists: bool, dry_run: bool = False) -> None:
    logger.info("Applying alembic migrations")
    config, script, context, script_head, current_head = get_alembic_config(conn)
    missing_revisions = [s for s in script.iterate_revisions(script_head, current_head)]

    if dry_run:
        if missing_revisions:
            logger.error("Database not updated. Please update with update_schema = True.")
        return

    if exists:
        if current_head != script_head:
            logger.info("Upgrading database to: %s", script_head)
            upgrade(config, "head")
            conn.commit()
        else:
            logger.info("The database is up-to-date: %s", script_head)
    elif script_head:
        logger.info("Stamping database with: %s", script_head)
        context.stamp(script, script_head)
        conn.commit()
    else:
        logger.warning("Unable to stamp database, check alembic revisions")


def initialize(update_schema: bool = False) -> None:
    from sqlalchemy import create_engine

    logger.info("Checking database connection and running migrations (sync)")
    sync_url = _get_sync_url(Config.database, suffix="?target_session_attrs=read-write")
    engine = create_engine(sync_url)
    with engine.connect() as conn:
        exists = _create_tables(conn, Config.database.ref_table, Config.database.force_recreate)
        _apply_migrations(conn, exists=exists, dry_run=not update_schema)

        if get_missing_revisions(conn) and update_schema:
            raise RuntimeError("Database is not up-to-date")
    engine.dispose()


@asynccontextmanager
async def session_scope():
    if async_session_factory is None:
        raise RuntimeError("Database not initialized. Call init() first.")
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Session rollback due to exception: {e}")
            raise DBError()
