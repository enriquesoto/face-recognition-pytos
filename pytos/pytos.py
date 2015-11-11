import constants,inspect,time,requests,pdb,os,csv,datetime,os,cv2,simplejson
import rpyc
from StringIO import StringIO
from cStringIO import StringIO
from PIL import Image
import numpy as np
import pytos_daemon as pd
import os
import inspect
import pytosdb
import time
import utils
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
			self.result = func(args,kwargs)
			end_time = time.time()
			timeLocally = end_time - start_time
			#paralelize
			methodBody = inspect.getsourcelines(func)
			methodDeclaration = utils.extractMethodDeclaration(methodBody)
			methodWeight = sys.getsizeof(methodBody)
			tasksRows = c.getTasks(methodDeclaration,methodWeight) #query if there is not enought remote calls information
			functionBody = inspect.getsource(func)
			
			if Task.getRemoteCalls(tasksRows) < constants.N_MIN_REMOTE_CALLS:
				print "enviando a cloudlet con fines estadisticos"
				task = Task(methodDeclaration,methodWeight,Solver.getSizeInBytes(args),timeLocally,functionBody)
			if Task.getLocalCalls(taskRows) < constants.N_MIN_LOCAL_CALLS:
				print "logging for stats"
				

	def persists(self):
		pass
	
	def start(self):
		self.prepare()
		self.decision()
		#self.persists()

def offload(func):
    def inner(*args,**kwargs):
		urlServer = constants.SERVER_ADDRESS+':'+str(constants.PORT)		

		
		#pdb.set_trace()
		db = pytosdb.PytosDB()
		os.system('python pytos/pytos_daemon.py &')
		
		off = Offloading(func,args,kwargs)

		argsObj = args[0]
		##basenamecvs = argsObj.basenamecvs
		#inputFolder = argsObj.pathInput
		#outputFolder = argsObj.pathOutput
		#testDataBasename = basenamecvs+'-'+str(now.month)+'-'+str(now.day)+'.csv'
		#offload = None
		conn = rpyc.connect("localhost", 22345)
		c = conn.root
		offload = c.getOffloadingDesicion()
		#offload = False
		if not offload:
			print "---> decorated function started locally"
			#testDataPath = constants.DATA_TEST_LOCAL+testDataBasename
			#with open(testDataPath,'a') as csvfile:
			#statsWriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
				#pdb.set_trace()
			start_time = time.time()
			result = func(*args,**kwargs)
			end_time = time.time()
			#total_time = end_time - start_time
			#total_time_list = []
			#total_time_list.append(argsObj.tmpImgFilebasename)
				#total_time_list.append(str(os.path.getsize(inputFolder + argsObj.tmpImgFilebasename)))
			#total_time_list.append(str(total_time))
			#statsWriter.writerow(total_time_list)
			print "--> decorated function ended locally"
			print("--- %s seconds ---" % (end_time - start_time))
			return result
		else:
			print "---> decorated function started remotelly"
		#testDataPath = constants.DATA_TEST_REMOTE+testDataBasename
		#with open(testDataPath,'a') as csvfile:
		#statsWriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			start_time = time.time()
			#pdb.set_trace()
				#func(*args,**kwargs)
			task='/heavyTask'
				#pathFile = args[0].__dict__.get("pathInput")
			openCVImage = args[1]
			restUrl = urlServer+task
			file = numpyArrayToStringIO(openCVImage)
			files = {'file':file }
			#files = numpyArrayToStringIO(openCVImage)
			r = requests.post(restUrl, files=files)
				#i = Image.open(StringIO(r.content))
				#i.save(outputWhenRemote+'/'+pathFile, "JPEG")
				#pathFile = "jeje.jpg"
				#basename = os.path.basename(pathFile)
				#i.save(outputFolder+basename, "JPEG")
			end_time = time.time()
			#total_time = end_time - start_time
			#total_time_list = []
			#total_time_list.append(str(getSizeInBytes(file)))
				#total_time_list.append(str())
			#total_time_list.append(str(total_time))
				#pdb.set_trace()
			facesTemp = StringIO(r.content) 
			#statsWriter.writerow(total_time_list)
			print "--> decorated function ended remotelly"
			print("--- %s seconds ---" % (end_time - start_time))
			return  simplejson.loads(facesTemp.read())


    return inner

def stringIOToNumpyArray(stringIO):
    #inmem_file = StringIO()
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
