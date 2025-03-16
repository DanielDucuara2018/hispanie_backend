import logging
from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path

from .utils import load_configuration, load_configuration_data

ROOT = Path(__file__).parents[1]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


@dataclass
class Database:
    database: str
    host: str
    password: str
    port: str
    user: str
    ref_table: str
    force_recreate: str = "0"


@dataclass
class JWT:
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str


@dataclass
class Email:
    secret_key: str
    security_password_salt: str
    frontend_url: str
    username: str
    password: str
    address: str
    port: str
    name: str
    server: str
    start_tls: str
    ssl_tls: str
    credentials: str
    validate_certs: str


@dataclass
class AWS:
    bucket_name: str
    access_key: str
    secret_key: str
    region: str


@dataclass
class Account:
    username: str
    password: str
    email: str
    phone: str
    description: str


@load_configuration
@dataclass
class Config:
    database: Database
    jwt: JWT
    email: Email
    aws: AWS
    account: Account


def bootstrap_configuration(path: str | Path = ROOT.joinpath("hispanie.ini")) -> None:
    logger.info("Loading configuration from file %s", path)
    config = ConfigParser()
    config.read(path)
    config_dict = {section: dict(config.items(section)) for section in config.sections()}
    load_configuration_data(config_dict)


bootstrap_configuration()
