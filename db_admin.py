from pymongo import MongoClient
import local_settings


class DBAdmin:
    def __init__(self) -> None:
        self.connect_to_db()

    def connect_to_db(self) -> None:
        self.client = MongoClient(host=local_settings.DATABASE['host'],
                                  port=local_settings.DATABASE['port'])
        self.db = self.client[local_settings.DATABASE['name']]
        self.collection = self.db['homegateDB']

    def add_info(self, arguments):
        for info in arguments:
            self.collection.insert_one(info)

    def get_info(self):
        return self.collection.find()
