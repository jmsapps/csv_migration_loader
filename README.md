# MongoDB Migration Setup

## Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python](https://www.python.org/)

## Getting Started

### 1. Start the MongoDB container

From the project root:

```sh
docker compose up -d
```

### 2. Setup Python
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Migrations
```sh
make migrate
```

### 4. Access the MongoDB container
```sh
docker exec -it local-mongo sh
```

### 5. Start the MongoDB shell Inside the container:
```sh
mongosh
```

### 6. View available databases Inside the `mongosh` shell:
```sh
show dbs
```
