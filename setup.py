# TODO remove setup.py deprecated

from setuptools import find_packages, setup

VERSION = "0.1"

INSTALL_REQUIRES = [
    "alembic>=1.14.0",
    "apischema>=0.19.0",
    "asyncio>=3.4.3",
    "bcrypt>=4.2.1",
    "fastapi[all]>=0.115.5",
    # "fastapi-utils",
    "psycopg2>=2.9.10",
    # "python-binance==1.0.16",
    "python-jose[cryptography]==3.3.0",
    # "python-telegram-bot==20.0a2",
    "SQLAlchemy>=2.0.36",
]

setup(
    name="hispanie",
    version=VERSION,
    python_requires=">=3.12.0",
    packages=find_packages(exclude=["tests"]),
    author="Daniel Ducuara",
    author_email="daniel14015@gmail.com",
    description="Backend for hispanie app",
    include_package_data=True,
    entry_points={"console_scripts": []},
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "dev": [
            "pre-commit>=4.0.1",
            "black>=24.10.0",
            "ruff>=0.8.0",
        ],
        "test": [
            "pytest>=8.3.3",
            "pytest-mock>=3.14.0",
            "pytest-cov>=6.0.0",
            "pytest-asyncio>=0.24.0",
        ],
    },
)
