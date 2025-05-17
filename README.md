# Hispanie Backend

The **Hispanie Backend** is the core server-side component of the Hispanie application, designed to manage and process data for the platform. Built with Python, it leverages modern development practices to ensure **scalability**, **maintainability**, and **ease of deployment**.

---

## 🚀 Features

- **Robust Backend Architecture**: Designed following clean architecture principles for maintainable codebases.
- **Dockerized Deployment**: Seamlessly deploy the entire stack using Docker and Docker Compose.
- **Pre-commit Hooks**: Automatically check code formatting and standards before each commit.
- **Database Integration**: Works with PostgreSQL for robust and scalable data persistence.

---

## 🛠️ Getting Started

### Prerequisites

Make sure the following tools are installed on your system:

- [Python 3.x](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [PostgreSQL](https://www.postgresql.org/)

---

### 🧪 Installation & Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/DanielDucuara2018/hispanie_backend.git
cd hispanie_backend
```

#### 2. Set Up Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Configure Pre-commit Hooks

```bash
pip install --user pre-commit
pre-commit install
pre-commit run --all-files
```

#### 4. Build and Launch Docker Containers

```bash
docker-compose up -d --build
```

#### 5. Create the Database

```bash
docker exec -it hispanie_backend-postgres-1 psql -U postgres -c "CREATE DATABASE hispanie;"
```

### 🌐 Network Configuration

#### 1. Add Host Entry

```bash
sudo nano /etc/hosts
# Add the following line:
169.254.10.2 hispanie
```

#### 2. Forward Local Port to Remote Server

```bash
ssh -L 127.0.0.1:3201:hispanie:3201 username@ip_address
```

### 📁 Project Structure

```bash
├── alembic/                 # Database migrations
├── hispanie/                # Application source code
├── pgsql/init.d/            # PostgreSQL initialization scripts
├── tests/                   # Unit and integration tests
├── Dockerfile               # Docker build configuration
├── docker-compose.yml       # Container orchestration
├── pyproject.toml           # Python project metadata
├── setup.py                 # Setup script for packaging
├── supervisord.conf         # Supervisor process config
└── README.md                # Project documentation
```

## 🤝 Contributing

Contributions are welcome!
If you'd like to improve or extend this project, please:

1. Fork the repository

2. Create a new feature branch

3. Submit a pull request with a clear description

## 📄 License

This project is licensed under the MIT License.
See the LICENSE file for more details.
