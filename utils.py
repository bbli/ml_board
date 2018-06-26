from pymongo import MongoClient
import ipdb 

def removeFolder(folder_name):
    client = safeMongoClient()
    client.drop_database(folder_name)
    client.close()

def removeRun(folder_name,run_name):
    client = safeMongoClient()
    client[folder_name][run_name].drop()
    client.close()

def viewFolder(folder_name):
    '''
    show all collections in a folder
    '''
    client = safeMongoClient()
    # include include_system_collections=False?
    for collection in client[folder_name].collection_names():
        print(collection)
    client.close()
def viewRun(folder_name,run_name):
    '''
    show all documents in a collection
    '''
    client = safeMongoClient()
    for doc in client[folder_name][run_name].find():
        print(doc)
    client.close()

def safeMongoClient():
    client = MongoClient()
    ipdb.set_trace()
    ## won't work because client is lazy loaded 
    if client== None:
        print("client is NoneType")
        raise "Cannot connect to MongoDB!"

class Database():
    def __init__(self):
        self.client = safeMongoClient()
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
