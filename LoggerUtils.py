from pymongo import MongoClient
from threading import Thread
import ipdb 

class Database():
    def __init__(self):
        self.client = safeMongoClient()
    ## Database utilities
    def removeFolder(self,folder_name):
        self.client.drop_database(folder_name)

    def removeRun(self,folder_name,run_name):
        self.client[folder_name][run_name].drop()

    def viewFolder(self,folder_name):
        '''
        show all collections in a folder
        '''
        # include include_system_collections=False?
        for collection in self.client[folder_name].collection_names():
            print(collection)
    def viewRun(self,folder_name,run_name):
        '''
        show all documents in a collection
        '''
        for doc in self.client[folder_name][run_name].find():
            print(doc)
    def close(self):
        self.client.close()
    ## Connection utilties
    def check_connection(self):
       t = Thread(target=self.test_insert,args=(self.experiment,)) 
       t.start()
       t.join(2)
       if t.is_alive():
           raise Exception("Cannot cannot to MongoDB")

    @staticmethod
    def test_insert(experiment):
        experiment.insert({"Test":1})
        experiment.remove({"Test":1})
if __name__ == '__main__':
    database = Database()
    database.client['test_db']['test_collection'].insert_one({"Test":"test"})
    database.viewRun('test_db','test_collection')
    database.removeRun('test_db','test_collection')
    database.viewRun('test_db','test_collection')
    
