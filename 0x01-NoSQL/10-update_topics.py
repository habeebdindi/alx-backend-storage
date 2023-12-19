#!/usr/bin/env python3
"""This module contains one function"""

if __name__ == "__main__":
    def update_topics(mongo_collection, name, topics):
        """function that changes all topics of a school document based on the name
        """
        mongo_collection.update_one(
            {'name': name}, {'$set': {'topics': topics}})