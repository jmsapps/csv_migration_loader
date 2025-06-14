from connection import dbConnection
from scripts import load_from_csv
from utils import coerce_items_by_validator

client = dbConnection()

def up():
    db = client["biopharma"]

    clinics_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "name", "short_name", "database"],
            "properties": {
                "_id": {
                    "bsonType": "int",
                    "description": "must be an integer and is required"
                },
                "name": {
                    "bsonType": "string",
                    "description": "full name of the clinic, required"
                },
                "short_name": {
                    "bsonType": "string",
                    "description": "short slug identifier, required"
                },
                "database": {
                    "bsonType": "string",
                    "description": "MongoDB database name associated with the clinic"
                }
            }
        }
    }

    clinics_collection = None
    try:
        clinics_collection = db.create_collection("clinics", validator=clinics_validator)
    except Exception as e:
        clinics_collection = db.get_collection("clinics")
        print(e)

    try:
        clinic_items = load_from_csv("csv/clinics.csv")
        coerced_clinic_items = coerce_items_by_validator(clinic_items, clinics_validator)
        clinics_collection.insert_many(coerced_clinic_items, ordered=False)
    except Exception as e:
        print(e)

        exit(1)

def down():
    db = client["biopharma"]

    db.drop_collection("clinics")
