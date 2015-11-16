from pytos.pytos import offload 
import numpy as np
import os,time,pdb,sys,constants

class Main:

	#pathInput = ''


	def __init__(self,imagesSource):
		self.settingsCascade = constants.HAAR_CASCADE_FILE #configuration file
		#self.basenamecvs = basenamecvs   # name of the file where stats will be written
		#self.offload = True if offload == 'remote' else False #offload to cloudlet or not
		self.imagesSource = imagesSource
	
	def start(self):
		#pdb.set_trace()
		if self.imagesSource == "video":
			self.startFromVideoCapture()
		if self.imagesSource == "directory":
			self.startFromDirectory()		
	
	def startFromDirectory(self):
		import cv2
		self.pathInput = constants.PATH_IMG_INPUT   #input folder where images will be taken from
		self.pathOutput = constants.PATH_IMG_OUTPUT  #output where imagens will be stored
		listing = os.listdir(self.pathInput)
		for file in listing:
			filePath = self.pathInput+file
			self.tmpImgFilebasename = os.path.basename(filePath)
			img = cv2.imread(filePath)
			faceCascade = cv2.CascadeClassifier(self.settingsCascade)
			faces = self.faceRecognition(img,faceCascade)
			if faces is not None:
				#pdb.set_trace()
				for (x,y,w,h) in faces:
					cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
				cv2.imwrite(self.pathOutput+'process'+self.tmpImgFilebasename,img)

	def startFromVideoCapture(self):
		#self.pathOutput = constants.PATH_IMG_OUTPUT  #output where imagens will be stored
		import cv2
		video_capture = cv2.VideoCapture(0)
		ret = video_capture.set(3,constants.VIDEO_WIDTH) #320
		ret = video_capture.set(4,constants.VIDEO_HEIGHT) #200
		width = video_capture.get(3) #real width
		height = video_capture.get(4) #real height
		fps_start_time = time.time()
		frameCountfps=0
		frameCount=0
		fps = 0
		while True:
		# Capture frame-by-frame
			frameCountfps += 1
			frameCount +=1
			ret, frame = video_capture.read()
			print "fps: %d" %fps
			faces = self.faceRecognition(frame)
			for (x,y,w,h) in faces:
				cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
			#cv2.imwrite(self.pathOutput+'process'+str(frameCount)+".jpg",frame)
			fps_end_time = time.time()
			if fps_end_time - fps_start_time > 1:
				#pdb.set_trace()
				fps = frameCountfps
				frameCountfps = 0
				fps_start_time = time.time()
			print "dimen %d x %d fps: %d" %(width,height,fps)
			#cv2.imshow('Video', frame)
		
	@staticmethod
	@offload #evaluate
	def faceRecognition(img,faceCascade):
		import cv2
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		#faceCascade = cv2.CascadeClassifier(self.settingsCascade)
		faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
		return faces

if __name__ == "__main__":
	if len(sys.argv) < 2:
		#print " you must enter 2 arguments!! in this order: basenameofcvs(time execution of decorated functions) local/remote video/directory"

		sys.exit()
	if len(sys.argv) == 2:
		imagesSourceOptions = ['video','directory']
	if sys.argv[1] not in imagesSourceOptions:
		print "bad request "
	x = Main(sys.argv[1]) #local
	x.start()

