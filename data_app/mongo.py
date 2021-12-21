from pymongo import MongoClient


def get_client(host="mongo", port=27017, maxPoolSize=200):
    return MongoClient(f"mongodb://root:example@{host}:{port}/", maxPoolSize=200)


def get_db(db="ldb"):
    return get_client()[db]


def get_collection(collection, db="ldb"):
    return get_db(db)[collection]
