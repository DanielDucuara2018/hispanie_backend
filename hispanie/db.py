import logging
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from alembic.command import upgrade
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from hispanie.model import Base

from .config import Database
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
    from .config import Config

    logger.info("Initialising postgres connection %s")
    engine = get_engine(Config.database)
    return sessionmaker(bind=engine)


def open_session(
    session_factory: sessionmaker,
) -> Session:
    return session_factory()


def get_alembic_config(conn: Connection):
    config = Config()
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


def create(conn: Connection):
    # Create tables
    logger.info("Creating tables %s", Base.metadata.tables.keys())
    Base.metadata.create_all(bind=conn)
    # Mark the db patchs as applied
    _, script, context, script_head, _ = get_alembic_config(conn)
    context.stamp(script, script_head)


def update(conn: Connection, table_name: str, dry_run: bool = False):
    """Apply missing revisions to the database."""
    config, _, _, script_head, current_head = get_alembic_config(conn)

    exists = True
    try:
        with conn.begin_nested():
            conn.execute(text(f"""SELECT 1 FROM {table_name} LIMIT 1"""))
    except Exception:  # TODO find the right exception
        exists = False

    if not dry_run:
        if not exists:
            create(conn)

        if current_head != script_head:
            upgrade(config, "head")
    else:
        return get_missing_revisions(conn)


def initialize(update_schema: bool = False) -> None:
    from .config import Config

    logger.info("Checking database connection")
    check_db_connection(Config.database)
    logger.info("Checking alembic migrations")
    engine = get_engine(Config.database, suffix="?target_session_attrs=read-write")

    exists = True
    try:
        with engine.connect() as conn:
            with conn.begin_nested():
                conn.execute(text(f"""SELECT 1 FROM {Config.database.ref_table} LIMIT 1"""))
    except Exception:  # TODO find the right exception
        exists = False

    if not exists:
        Base.metadata.create_all(engine)

    # TODO fix create_all process + alembic migrations. Not working
    # applied_revisions = update(conn, db.ref_table, dry_run=not update_schema)

    # if applied_revisions and update_schema:
    #     raise RuntimeError("Database is not up-to-date")


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
