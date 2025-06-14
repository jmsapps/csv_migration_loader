from pymongo import MongoClient

def dbConnection() -> MongoClient:
    return MongoClient("mongodb://localhost:27017/")
