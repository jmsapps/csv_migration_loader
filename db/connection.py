from pymongo import MongoClient

from utils import getenv


def dbConnection() -> MongoClient:
    environment = getenv("environment", "development")
    user = getenv("DB_USER")
    password = getenv("DB_PASS")
    host = getenv("DB_HOST")
    port = getenv("DB_PORT")
    params = "ssl=true&replicaSet=rs0&readPreference=secondaryPreferred"

    uri = f"mongodb://{user}:{password}@{host}:{port}"

    if environment == "production":
        uri = f"{uri}/?{params}"

        return MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)

    return MongoClient(uri)
