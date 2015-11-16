import constants,inspect,time,requests,pdb,os,csv,datetime,os,cv2,simplejson
import rpyc
from StringIO import StringIO
from cStringIO import StringIO
from PIL import Image
import numpy as np
from pytos_daemon import Solver
import os
import inspect
import pytosdb
import time
from utils import Utils
import sys

class Offloading:
    func = None
    args = None
    task = None
    args = None
    kwargs = None
    result = None
    def __init__(self,func,args,kwargs):
        self.func=func
        self.args=args
        self.kwargs=kwargs
    def prepare(self):
        os.system('python pytos/pytos_daemon.py &')
        db = pytosdb.PytosDB() #create initial DB
    def decision(self):
        conn = rpyc.connect("localhost", 22345)
        c = conn.root
        offload = c.getOffloadingDesicion()
        if not offload:
            start_time = time.time()
            self.result = self.func(*self.args,**self.kwargs)
            end_time = time.time()
            timeLocally = end_time - start_time
            #paralelize create a new thread
            methodBody = inspect.getsourcelines(self.func)
            methodDeclaration = Utils.extractMethodDeclaration(methodBody)
            methodWeight = sys.getsizeof(methodBody)
            #tasksRows = c.getTasks(methodDeclaration,methodWeight) #query if there is not enought remote calls information
            tasksRows = pytosdb.TaskDAO.getTasksByProperties(methodDeclaration,methodWeight)
            functionBody = inspect.getsource(self.func)
            if pytosdb.TaskDAO.getRemoteCalls(tasksRows) < constants.N_MIN_REMOTE_CALLS:
                print "enviando a cloudlet con fines estadisticos"
            if pytosdb.TaskDAO.getLocalCalls(tasksRows) < constants.N_MIN_LOCAL_CALLS:
                print "logging for stats"
                argument= self.args[1]
                argsSize = Solver.getSizeInBytes(argument)
                task = pytosdb.Task(methodDeclaration,methodWeight,argsSize,timeLocally,functionBody)
                taskDAO = pytosdb.TaskDAO(task)
            
    def start(self):
        self.prepare()
        self.decision()

def offload(func):
    def inner(*args,**kwargs):
        pdb.set_trace()
        urlServer = constants.SERVER_ADDRESS+':'+str(constants.PORT)
        offloading = Offloading(func,args,kwargs)
        offloading.start()
        db = pytosdb.PytosDB()
        os.system('python pytos/pytos_daemon.py &')
        conn = rpyc.connect("localhost", 22345)
        c = conn.root
        offload = c.getOffloadingDesicion()
        if  True:
            print "---> decorated function started locally"
            start_time = time.time()
            result = func(*args,**kwargs)
            end_time = time.time()
            print "--> decorated function ended locally"
            print("--- %s seconds ---" % (end_time - start_time))
            return result
        else:
            print "---> decorated function started remotelly"
            start_time = time.time()
            task='/heavyTask'
            openCVImage = args[1]
            restUrl = urlServer+task
            file = numpyArrayToStringIO(openCVImage)
            files = {'file':file }
            r = requests.post(restUrl, files=files)
            end_time = time.time()
            facesTemp = StringIO(r.content) 
            print "--> decoraed function ended remotelly"
            print("--- %s seconds ---" % (end_time - start_time))
            return  simplejson.loads(facesTemp.read())
    return inner

def stringIOToNumpyArray(stringIO):
    #inmem_fle = StringIO()
    #fileStorage.save(inmem_file)  # save to memory
    #inmem_file.reset()  # seek back to byte 0, otherwise .read() will return ''
    #pdb.set_trace()
    file_bytes = np.frombuffer(stringIO.read(), np.uint8)
    #file_bytes = np.asarray(bytearray(stringIO.read()), dtype=np.uint8)
    #numpyArray = cv2.imdecode(file_bytes, cv2.CV_LOAD_IMAGE_UNCHANGED)
    numpyArray = cv2.imdecode(file_bytes,1)
    return numpyArray

def numpyArrayToStringIO(numpyArray):
    img_str = cv2.imencode('.jpg', numpyArray)[1].tostring()
    response = StringIO(img_str)
    return response
def getSizeInBytes(stringIO):
    
    stringIO.seek(0, os.SEEK_END)
    bytesCount = stringIO.tell()
    stringIO.seek(0)
    return bytesCount
