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
from utils import Utils
#development
import pdb

class Global():
  offloading=False
  cloudleAvailable = True
  idleTime=0

class MyService(rpyc.Service):
  def exposed_getOffloadingDesicion(self,argsSize):
    main.iddleTime=0
    return main.offloading
  def exposed_getTasks(self,methodDeclaration,methodWeight): # returns how many tasks left to complete the minium quantity to forecast the expected time
    nTasks = pytosdb.TaskDAO.getTasksByProperties(methodDeclaration,methodWeight)
    return nTasks
if __name__ == '__main__':
  me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running
  server = ThreadedServer(MyService, port = 22345)
  t = Thread(target = server.start)
  t.daemon = True
  t.start()
  # the main logic
  main = Global()
  pytosDaemon = PytosDaemon()
  main.offloading = False

  while True:
    if main.idleTime >= constants.KILLINGTIME: #if its iddle by killingTime constants, pytos daemon is killed
      sys.exit()
    main.idleTime += constants.TIMEGAP
    pytosDaemon.start()
    time.sleep(constants.TIMEGAP)

class PytosDaemon():
  self.cloudlet = None
  def __init__(self):
    pass
  def discoverer(self):
    pass
  def solver(self, argList):
    argsSize=0
    for arg in argList:
      argSize+=self.getSizeInBytes(arg)
  def profiler(self,taskId):
    pass

class Cloudlet:
  def __init__(self):
    pass
