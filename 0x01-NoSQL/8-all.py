#!/usr/bin/env python3
"""This module contains one function"""


if __name__ == "__main__":
    def list_all(mongo_collection):
        """returns a list all documents in a collection"""
        result = mongo_collection.find()
        if not result:
            return []
        return result
