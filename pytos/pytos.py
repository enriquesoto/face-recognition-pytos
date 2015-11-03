import constants,inspect,time,requests,pdb,os,csv,datetime,os,cv2,simplejson
from StringIO import StringIO
from cStringIO import StringIO
from PIL import Image
import numpy as np
import pytos_daemon as pd
import os

def offload(func):
    def inner(*args,**kwargs):
		urlServer = constants.SERVER_ADDRESS+':'+str(constants.PORT)		
		os.system('python pytos/pytos_daemon.py &')
		argsObj = args[0]
		##basenamecvs = argsObj.basenamecvs
		#inputFolder = argsObj.pathInput
		#outputFolder = argsObj.pathOutput
		#testDataBasename = basenamecvs+'-'+str(now.month)+'-'+str(now.day)+'.csv'
		#offload = None
		offload = True
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
