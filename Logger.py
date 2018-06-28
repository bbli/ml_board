from pymongo import MongoClient
import datetime
from LoggerUtils import *
import ipdb


class SummaryWriter(Database):
    def __init__(self,folder_name,run_name=None):
        super().__init__()
        if run_name == None:
            run_name = datetime.datetime.now().strftime("%B %d, %Y at %I:%M%p")

        self.experiment = self.client[folder_name][run_name]
        

    def add_scalar(self,variable_name:str, f:int):
        self.experiment.update_one({variable_name:{"$exists":"true"}}, {'$push' :{variable_name:f}}, upsert=True)

    def add_experiment_parameter(self,parameter_name:str, value:int):
        self.experiment.update_one({"Parameters":{"$exists":"true"}}, {'$push':{'Parameters':{parameter_name:value}}}, upsert=True)
    def viewRun(self):
        '''
        show all the data logged from the run
        '''
        for doc in self.experiment.find():
            print(doc)


        

if __name__ == '__main__':
    w = SummaryWriter('test')
    w.add_experiment_parameter('Learning Rate',2)
    w.add_experiment_parameter('Neurons',3)
    for i in range(5):
        w.add_scalar("Loss",i**2)
    w.viewFolder('test')
    w.viewRun()
    ipdb.set_trace()
    w.removeFolder('test')
    w.close()


