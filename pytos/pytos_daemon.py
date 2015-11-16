# main definitions
import time
import rpyc
import sys
import constants
from tendo import singleton
from rpyc.utils.server import ThreadedServer
from threading import Thread
import pytosdb
import cStringIO
import cv2
import numpy as np
from cStringIO import StringIO
import os
#development
import pdb

class Global():
	offloading=False
	idleTime=0

class MyService(rpyc.Service):
	def exposed_getOffloadingDesicion(self):
		main.iddleTime=0
		return main.offloading
	def exposed_getTasks(self,methodDeclaration,methodWeight): # returns how many tasks left to complete the minium quantity to forecast the expected time
		nTasks = pytosdb.TaskDAO.getTasksByProperties(methodDeclaration,methodWeight)
		#return constants.N_FIRST_REMOTE_CALLS-len(nTasks)
		return nTasks
if __name__ == '__main__':
	me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running
	server = ThreadedServer(MyService, port = 22345)
	t = Thread(target = server.start)
	t.daemon = True
	t.start()

# the main logic
	main = Global()
	while True:
		if main.idleTime >= constants.killingTime:
			sys.exit()
		main.idleTime += constants.timeGap 
		main.offloading =False
		time.sleep(constants.timeGap)

class Solver():
	def __init__(self):
		pass
	def forecast(self, argList):
		argsSize=0
		for arg in argList:
			argSize+=self.getSizeInBytes(arg)

	@staticmethod
	def getSizeInBytes(var):
		if type(var).__module__ == np.__name__:
			response = 0
			cstringvar = Solver.numpyArrayToStringIO(var)
	#if isinstance(var, cStringIO.InputType):
			cstringvar.seek(0, os.SEEK_END)
			response = cstringvar.tell()
			cstringvar.seek(0)
		else:
			response = sys.getsizeof(var)
		return response
	
	@staticmethod
	def numpyArrayToStringIO(numpyArray):
		#pdb.set_trace()$
		if len(numpyArray) == 0:
			return StringIO('')
		img_str = cv2.imencode('.jpg', numpyArray)[1].tostring()
		response = StringIO(img_str)
		return response

	def model(self,taskId):
		pass
