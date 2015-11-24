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
import requests
import Pyro4
#development
import pdb

class Global():
  offloading=True
  uriCloudlet = None
  idleTime=0
  ssid = None
  weight =None
  bandwidth = 0
  ipl = {}

class PytosDaemon():
  mainGlobals = None
  cloudlet = None
  def __init__(self,main):
    self.mainGlobals = main
  def discover(self):
    response = requests.get(constants.URI_DISCOVERY_ENDPOINT+self.mainGlobals.ssid)
    code = response.status_code
    if code is 200:
      main.uriCloudlet = str(response.json()["cloudlet"]["uri"])
    else:
      main.uriCloudlet = None

  def profile(self):
    if self.mainGlobals.uriCloudlet is not None:
      remoteCall = Pyro4.Proxy(self.mainGlobals.uriCloudlet)
      start_time = time.time()
      ans = remoteCall.measureBandwidth(self.mainGlobals.weight)
      total_time = time.time()-start_time
      bandwidth = Utils.getSizeInBytes(self.mainGlobals.weight)/total_time
    #pdb.set_trace()
    tasks = pytosdb.TaskDAO.getAllTasks()
    if len(tasks) > 0:
      #pdb.set_trace()
      for task in tasks:
        result = pytosdb.TaskDAO.getExecutionsTimes(str(task[0]),task[1])
        if len(result) >0:
          ans = np.array(result) #fx
          self.mainGlobals.ipl[str(task[0])+str(task[1])+"_local"] = np.polyfit(ans[:,0],ans[:,1],1)
          self.mainGlobals.ipl[str(task[0])+str(task[1])+"_remote"] =  np.polyfit(ans[:,0],ans[:,2],1)

  def solve(self, methodSignature, methodWeight, argsSize):
    if self.mainGlobals.uriCloudlet is not None and len(self.mainGlobals.ipl)>0:
      localPoly = self.mainGlobals.ipl[methodSignature+str(methodWeight)+"_local"]
      remotePoly = self.mainGlobals.ipl[methodSignature+str(methodWeight)+"_remote"]
      localTimeForecast = localPoly[0]*argsSize+localPoly[1]
      remoteTimeForecast = remotePoly[0]*argsSize+remotePoly[1]+argsSize*self.mainGlobals.bandwidth
      if (remoteTimeForecast < localTimeForecast):
        return True
    return False

  def start(self):
    self.discover()
    self.profile()

class MyService(rpyc.Service):
  def exposed_getOffloadingDesicion(self,methodSignature, methodWeight, argsSize):
    main.iddleTime=0
    return pytosDaemon.solve(methodSignature, methodWeight, argsSize)
  def exposed_getUri(self):
    return main.uriCloudlet

if __name__ == '__main__':
  me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running
  Pyro4.config.SERIALIZERS_ACCEPTED.add("pickle")
  Pyro4.config.SERIALIZER="pickle"
  server = ThreadedServer(MyService, port = 22345)
  t = Thread(target = server.start)
  # the main logica
  main = Global()
  main.weight = cv2.imread(constants.WEIGHT_FILE)
  pytosDaemon = PytosDaemon(main)
  t.daemon = True
  t.start()

  while True:
    if main.idleTime >= constants.KILLING_TIME: #if its iddle by killingTime constants, pytos daemon is killed
      sys.exit()
    main.idleTime += constants.TIMEGAP
    main.ssid = Utils.getSSID()
    pytosDaemon.start()
    time.sleep(constants.TIMEGAP)

