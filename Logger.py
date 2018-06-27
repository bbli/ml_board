from pymongo import MongoClient
import datetime
from LoggerUtils import *
import ipdb


class SummaryWriter(Database):
    def __init__(self,folder_name,run_name=None):
        # super().__init__()
        self.client = MongoClient()

        if run_name == None:
            run_name = datetime.datetime.now().strftime("%B %d, %Y at %I:%M%p")

        self.experiment = self.client[folder_name][run_name]
        self.check_connection()

        self.experiment.insert({"Name of Text":"Experimental Parameters","Parameters": [{"Time":run_name}]})
        # self.experiment.insert({'id':'id','Test':[1]})
        # self.experiment.update({'id':'id'},{'$push':{'Test':2}})
        

    def add_scalar(self,variable_name:str, f:int, t:int):
        '''
        add a new datapoint to the collection. Make sure to start t at 0
        '''
        # self.experiment.insert({'Variable name':variable_name,'f':f,'t':t})

        if t==0:
            self.experiment.insert({'Variable name':variable_name,'f':[f],'t':[t]})
        else:
            self.experiment.update({'Variable name':variable_name},{'$push' :{"t" : t }})
            self.experiment.update({'Variable name':variable_name},{'$push' :{"f" : f }})

    def add_experiment_parameter(self,parameter:str, value:int):
        # self.experiment.insert({'Experimental Parameters':'Experimental Parameters',parameter:value})

        self.experiment.update({'Name of Text':"Experimental Parameters"},{'$push' :{'Parameters' : {parameter:value} }})
        # if t==0:
            # self.experiment.insert({'Name of Text':name_of_text,'Parameters':[{parameter:value}]})
        # else:
            # self.experiment.update({'Name of Text':name_of_text},{'$push' :{'Parameters' : {parameter:value} }})
    def viewRun(self):
        '''
        show all the data logged from the run
        '''
        for doc in self.experiment.find():
            print(doc)


        

if __name__ == '__main__':
    w = SummaryWriter('test')
    w.add_experiment_parameter('Learning Rate',2)
    w.add_experiment_parameter('Learning Rate',3)
    for i in range(5):
        w.add_scalar("Loss",i**2,i)
    w.viewFolder('test')
    w.viewRun()
    ipdb.set_trace()
    w.removeFolder('test')
    w.close()


