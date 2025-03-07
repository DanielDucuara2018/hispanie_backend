# Hispanie

Backend for hispanie app

## DB creation

```bash
docker exec -it hispanie_backend-postgres-1 psql -U postgres -c "CREATE DATABASE hispanie;"
```

## pre-commit

```bash
pip install --user pre-commit
pre-commit install
pre-commit run --all-files
```

## pytho venv

```bash
python3 -m venv venv
```

## generate docker containers

```bash
docker-compose up -d --build
```

## forwarding ports

Create a host name for hispanie application:

```bash
sudo nano /etc/hosts
169.254.10.2 hispanie
```

Forward port in host machine:

```bash
ssh -L 127.0.0.1:3201:hispanie:3201 username@ip_address
```

## Build docker image for production

```bash
docker-compose build
docker tag hispanie_backend-app europe-west4-docker.pkg.dev/hispanie/hispanie-docker/hispanie_backend-app:0.1
```

## Push docker production image

```bash
docker push europe-west4-docker.pkg.dev/hispanie/hispanie-docker/hispanie_backend-app:0.1
```
