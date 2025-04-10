from contextlib import contextmanager
from pathlib import Path

from psycopg2 import errors as pgsql_errors
from sqlalchemy import text
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.exc import SQLAlchemyError, StatementError
from sqlalchemy.orm import Session, sessionmaker

from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory

from .config import Config, Database, logging
from .errors import DBError

ROOT = Path(__file__).parents[1]
ALEMBIC_PATH = ROOT.joinpath("alembic")

logger = logging.getLogger(__name__)


def get_engine(db: Database, suffix: str | None = None) -> Engine:
    sqlalchemy_url = f"postgresql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}"
    if suffix:
        sqlalchemy_url += suffix
    return create_engine(sqlalchemy_url)


def check_db_connection(db: Database) -> None:
    conn = get_engine(db).connect()
    conn.close()


def init() -> sessionmaker:
    logger.info("Initialising database session")
    engine = get_engine(Config.database)
    return sessionmaker(bind=engine)


def open_session(
    session_factory: sessionmaker,
) -> Session:
    return session_factory()


def get_alembic_config(conn: Connection):
    config = AlembicConfig()
    config.attributes["connection"] = conn
    config.set_section_option("alembic", "script_location", str(ALEMBIC_PATH))
    script = ScriptDirectory.from_config(config)
    context = MigrationContext.configure(conn)
    script_head = script.get_current_head()
    current_head = context.get_current_revision()

    return config, script, context, script_head, current_head


def get_missing_revisions(conn: Connection):
    _, script, _, script_head, current_head = get_alembic_config(conn)
    return [s for s in script.iterate_revisions(script_head, current_head)]


def create(conn: Connection, table_name: str, force: bool) -> bool:
    """Check the database and create it if necessary."""
    exists = True
    try:
        with conn.begin_nested():
            conn.execute(text(f"select 1 from {table_name} limit 1"))
    except StatementError as e:
        if isinstance(e.orig, pgsql_errors.UndefinedTable):
            exists = False
        else:
            raise

    if not exists or force:
        from .model import Base

        logger.info("Creating all tables %s", list(Base.metadata.tables))
        Base.metadata.create_all(bind=conn)

    return exists


def update(conn: Connection, exists: bool, dry_run: bool = False) -> None:
    """Apply missing revisions to the database."""
    logger.info("Applying alembic migrations")
    config, script, context, script_head, current_head = get_alembic_config(conn)
    missing_revisions = [s for s in script.iterate_revisions(script_head, current_head)]

    if dry_run and missing_revisions:
        logger.error("Database not updated. Please update with update_schema = True.")

    if exists:
        if current_head != script_head:
            logger.info("Upgrading database to: %s", script_head)
            upgrade(config, "head")
            conn.commit()
        else:
            logger.info("The database is up-to-date: %s", script_head)
    elif script_head:
        logger.info("Stamping database with: %s", script_head)
        # Mark the db patchs as applied
        context.stamp(script, script_head)
        conn.commit()
    else:
        logger.warning("Unable to stamp database, check alembic revisions")


def initialize(update_schema: bool = False) -> None:
    logger.info("Checking database connection")
    check_db_connection(Config.database)

    logger.info("Checking alembic migrations")
    engine = get_engine(Config.database, suffix="?target_session_attrs=read-write")
    with engine.connect() as conn:
        exists = create(conn, Config.database.ref_table, bool(int(Config.database.force_recreate)))
        update(conn, exists=exists, dry_run=not update_schema)

        if get_missing_revisions(conn) and update_schema:
            raise RuntimeError("Database is not up-to-date")


session = open_session(init())


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Session rollback due to exception: {e}")
        raise DBError()
