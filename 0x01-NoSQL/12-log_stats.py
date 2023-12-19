#!/usr/bin/env python3
"""THis module contains one function
"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("{} logs".format(collection.count_documents({})))
    print("Methods:")
    for m in methods:
        method = collection.find({"method": m})
        count = collection.count_documents({"method": m})
        print("\tmethod {}: {}".format(m, count))
    print("{} status check".format(
        collection.count_documents({"method": "GET", "path": "/status"}))
    )
