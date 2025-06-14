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

### 3. Add Normalization Fields for load_from_csv.py script
- Copy `scripts/normalization_fields.py.example` => `scripts/normalization_fields.py`
- Add additional normalization fields ass necessary (normalizes csv headers e.g. 'somecolumnheader' to 'some_column_header')

### 4. Create and Run Migrations
Create migration (a file will be created in db/migrations with an up() and down() function and client connection):
```sh
make migrate_create name="init_db"
```

Run the up() migration (versions will be tracked in db/migrations/.current):
```sh
make migrate
```

Rollback using the down() migration:
```sh
make migrate_down
```

If you want to leverage the load_from_csv_script you can do so like this:
```py
from connection import dbConnection
from scripts import load_from_csv
from utils import coerce_items_by_validator

client = dbConnection()

def up():
    db = client["your_database"]

    users_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "username", "email", "role"],
            "properties": {
                "_id": {
                    "bsonType": "int",
                    "description": "Must be an integer and is required"
                },
                "username": {
                    "bsonType": "string",
                    "description": "Username of the user"
                },
                "email": {
                    "bsonType": "string",
                    "description": "Email address of the user"
                },
                "role": {
                    "bsonType": "string",
                    "description": "Role assigned to the user"
                }
            }
        }
    }

    users_collection = None
    try:
        users_collection = db.create_collection("users", validator=users_validator)
    except Exception as e:
        users_collection = db.get_collection("users")
        print(e)

    try:
        user_items = load_from_csv("csv/users.csv")
        coerced_user_items = coerce_items_by_validator(user_items, users_validator)
        users_collection.insert_many(coerced_user_items, ordered=False)
    except Exception as e:
        print(e)

def down():
    db = client["your_database"]
    db.drop_collection("users")
```

You can even use `coerce_items_by_validator` to coerce types, leveraging the $jsonSchema object.

___Note__: Don't forget to add your csv files to `csv/` if you want to create migrations using those files._

### 5. Access the MongoDB container
```sh
docker exec -it local-mongo sh
```

### 6. Start the MongoDB shell inside the container:
```sh
mongosh
```

### 7. View migrations inside the `mongosh` shell:
```sh
show dbs
```
