# main definitions
import time
import rpyc
import sys
import constants
from tendo import singleton
from rpyc.utils.server import ThreadedServer
from threading import Thread
import pytosdb
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
		#pdb.set_trace()
		nTasks = Task.getTasksByProperties(self,methodDeclaration,methodWeight)
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
			argSize+=getSizeInBytes(arg)

	
	def getSizeInBytes(self,var):
		response = 0
		if isinstance(var, cStringIO.InputType):
			stringIO.seek(0, os.SEEK_END)
			response = stringIO.tell()
			stringIO.seek(0)
		else:
			response = sys.getsizeof(var)
		return response
	def model(self,taskId):
		pass
