from pymongo import MongoClient
import datetime
from utils import *
import ipdb


class SummaryWriter(Database):
    def __init__(self,folder_name,run_name=None):
        # super().__init__()
        # self.client = MongoClient()
        self.client = safeMongoClient()

        if run_name == None:
            run_name = datetime.datetime.now().strftime("%B %d, %Y at %I:%M%p")

        self.experiment = self.client[folder_name][run_name]

        ## convert to better format for regex/datetime comparisons
        self.add_experiment_parameter("Time",run_name)

    def add_scalar(self,variable_name:str, f:int, t:int):
        '''
        add a new datapoint to the collection
        '''
        self.experiment.insert({'Variable name':variable_name,'f':f,'t':t})

    def add_experiment_parameter(self,parameter:str, value:int):
        self.experiment.insert({'Experimental Parameters':'Experimental Parameters',parameter:value})
        

if __name__ == '__main__':
    w = SummaryWriter('test')
    w.add_experiment_parameter('Learning Rate',2)
    for i in range(5):
        w.add_scalar('Loss',2*i,i)
    w.viewFolder('test')
    ipdb.set_trace()
    w.close()
    w.removeFolder('test')


