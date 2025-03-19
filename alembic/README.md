# Alembic
Alembic is a database migration tool for SQLAlchemy, which allows you to manage database schema changes in a version-controlled and reversible way. Here are some of the most commonly used commands in Alembic:

## Installation
Normally `alembic` is already installed as it is a required package. Just check as follows::

```
alembic --version
```
And the `version` must be greater than or equal to `1.4.3`.

## Creating a Migration
To create a new migration, just position yourself in the alembic folder.

```bash
cd alembic
```

To create migration run the revision command:

```
alembic revision --autogenerate -m "The revision change message"
```

This will generate a new migration script based on the current state of your database schema. You can then edit the script to make any necessary changes.

#### Local Development Setup

To ensure the application connects to your local PostgreSQL instance during development, add the following line to your `/etc/hosts` file: 127.0.0.1 postgres

This will resolve the hostname `postgres` to your local machine (localhost).  You'll need administrator privileges to modify `/etc/hosts`.  Here's how you can typically do it:

```bash
sudo echo "127.0.0.1        postgres" >> /etc/hosts
```

Or simply modify the database host configuration within `hispanie.ini`.  Change the `database.host` value from `postgres` to `localhost`.


## Upgrading and Downgrading
To upgrade your database schema to the latest version, use the upgrade command:

```
alembic upgrade head
```

This will apply all of the migrations that haven't been applied yet.

To downgrade your database schema to a previous version, use the downgrade command:

```
alembic downgrade -1
```

This will undo the last migration that was applied.

## Viewing the Current Revision
To view the current revision of your database schema, use the current command:

```
alembic current
```

This will show you the current version number of your database schema.

## Generating SQL
To generate SQL for a migration without actually applying it, use the upgrade command with the `--sql` flag as follow:

```
alembic upgrade head --sql
```

This will generate SQL that would be executed if you were to apply the migration.

## Other Commands
There are many other commands available in Alembic, including `history`, `show`, and `stamp`. You can view a full list of commands by running:

```
alembic --help
```

## Documentation
For more information: [link doc](https://alembic.sqlalchemy.org/en/latest/)
