from pymongo import MongoClient
import datetime
from Utils import Database
import ipdb
from bson.binary import Binary
# import cPickle
import pickle

class SummaryWriter(Database):
    def __init__(self,database_name,folder_name):
        super().__init__()
        self.database_name = database_name
        self.folder_name = folder_name
        self.runs = self.client[database_name][folder_name]

        self.date = datetime.datetime.today().strftime("%Y-%m-%d-%H:%M:%S")
        self.runs.insert_one( {"Experimental Parameters":{"Time":self.date}})
        # self.runs.update_one({"Experimental Parameters.Time":self.date},{'$set':{"Time":self.date}})

    def add_scalar(self,variable_name:str, f:int):
        self.runs.update_one({"Experimental Parameters.Time":self.date},{'$push':{"Plots."+variable_name:f}},upsert= True)
    def add_histogram(self, histogram_name:str, f:int):
        self.runs.update_one({"Experimental Parameters.Time":self.date},{'$push':{"Histograms."+histogram_name:f}},upsert= True)
    def add_image(self,image_name,image):
        processed_image = Binary(pickle.dumps(image,protocol=2))
        self.runs.update_one({"Experimental Parameters.Time":self.date},{'$set':{"Images."+image_name:processed_image}},upsert= True)
    def add_experiment_parameter(self, parameter_name:str, value:int):
        self.runs.update_one({"Experimental Parameters.Time":self.date}, {'$set':{"Experimental Parameters."+parameter_name:value}})
    def add_thought(self,string):
        self.runs.update_one({"Experimental Parameters.Time":self.date},{'$push':{"Thoughts":self.folder_name}},upsert= True)
        self.runs.update_one({"Experimental Parameters.Time":self.date},{'$push':{"Thoughts":string}},upsert= True)
    def viewRun(self):
        '''
        show all the data logged from the run
        '''
        for doc in self.runs.find({"Experimental Parameters.Time":self.date}):
            print(doc)


        

if __name__ == '__main__':
    w = SummaryWriter('test_db','test_collection')
    w.add_experiment_parameter('Learning Rate',2)
    w.add_experiment_parameter('Neurons',3)
    for i in range(5):
        w.add_scalar("Loss",i**2)
    w.add_thought("hi")
    w.add_thought("hello")
    w.viewRun()
    # ipdb.set_trace()
    # w.removeFolder('test_db','test_collection')
    # w.close()


