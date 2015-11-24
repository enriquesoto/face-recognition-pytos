import numpy as np
from cStringIO import StringIO
import cStringIO
import constants
import sys
import cv2
import os

class Utils:

  @staticmethod
  def getSizeInBytes(var):
    response = 0
    if type(var).__module__ == np.__name__:
      cstringvar = Utils.numpyArrayToStringIO(var)
      #if isinstance(var, cStringIO.InputType):
      cstringvar.seek(0, os.SEEK_END)
      response = cstringvar.tell()
      cstringvar.seek(0)
    else:
      response = sys.getsizeof(var)
    return response

  @staticmethod
  def getArgsSize(var):
    size = 0
    for k in var:
      s1 = Utils.getSizeInBytes(k) 
      size = size + Utils.getSizeInBytes(k)
    return size
  
  @staticmethod
  def numpyArrayToStringIO(numpyArray):
    if len(numpyArray) == 0:
      return StringIO('')
    img_str = cv2.imencode('.jpg', numpyArray)[1].tostring()
    response = StringIO(img_str)
    return response

  @staticmethod
  def getSSID():
    from wireless import Wireless
    wireless = Wireless()
    return  wireless.current()


  
 

