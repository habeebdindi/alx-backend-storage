#!/usr/bin/env python3
"""This module contains one function"""


if __name__ == "__main__":
    def insert_school(mongo_collection, **kwargs):
        """function that inserts a new document in a collection based on kwargs"""
        result = mongo_collection.insert_one(kwargs)
        return result.inserted_id
