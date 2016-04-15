from threading import Thread
#import picamera
import cv2
import numpy as np
import time
import grovepi
import heapq
import os
from time import sleep


triggerFound = False



class streamMedian:
    def __init__(self):
        self.minHeap, self.maxHeap = [], []
        self.N = 0

    def insert(self, num):
        if self.N % 2 == 0:
            heapq.heappush(self.maxHeap, -1 * num)
            self.N += 1
            if len(self.minHeap) == 0:
                return
            if -1 * self.maxHeap[0] > self.minHeap[0]:
                toMin = -1 * heapq.heappop(self.maxHeap)
                toMax = heapq.heappop(self.minHeap)
                heapq.heappush(self.maxHeap, -1 * toMax)
                heapq.heappush(self.minHeap, toMin)
        else:
            toMin = -1 * heapq.heappushpop(self.maxHeap, -1 * num)
            heapq.heappush(self.minHeap, toMin)
            self.N += 1

    def getMedian(self):
        if self.N % 2 == 0:
            return (-1 * self.maxHeap[0] + self.minHeap[0]) / 2.0
        else:
            return -1 * self.maxHeap[0]



def detectCrosswalkLines(resizedInputPhoto):
    print "Detect crosswalk lines start"
    croppedInputPhoto = resizedInputPhoto[height / 2:height, :]
    gray_img = cv2.cvtColor(croppedInputPhoto, cv2.COLOR_BGR2GRAY)
    ret, gray_img = cv2.threshold(gray_img, 150, 255, cv2.THRESH_BINARY)
    img, contours, _ = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    numContours = len(contours)
    possibleLines = {}
    midptMedian = streamMedian()
    if numContours > 0:
        for i in range(0, numContours):
            area = cv2.contourArea(contours[i], False)
            if area > 100:
                x, y, w, h = cv2.boundingRect(contours[i])
                midPt = (x + x + w) / 2

                midptMedian.insert(midPt)
                possibleLines[i] = [x, y, w, h]

    crossLineContourIndexes = []
    median = midptMedian.getMedian()
    # print "ok, done. median is: ", median
    for key, val in possibleLines.iteritems():
        x = val[0]
        w = val[2]

        midPt = (x + x + w) / 2
        # print "MIDPT for {} is {}".format(key, midPt)
        if ((median - 40) <= midPt <= (median + 40)):
            crossLineContourIndexes.append(key)

    if len(crossLineContourIndexes) > 3:
        global triggerFound
        triggerFound = True
        print "Crosswalk lines found"
        for contour in crossLineContourIndexes:
            cv2.drawContours(croppedInputPhoto, contours, contour, (0,255,0), 3)
    cv2.imshow('crosswalk lines contours', croppedInputPhoto)
    cv2.waitKey(30)




#functions
def detectStopSign(resizedInputPhoto):
        print "Stop sign start"
	#%--------------------THRESHOLD IMAGE--------------------%
        threeFourthsDown = resizedInputPhoto.shape[0] * (3.0 / 4)
        croppedInputPhoto = resizedInputPhoto[0:threeFourthsDown, :]
	for i in range(0, croppedInputPhoto.shape[0]):
		for j in range(0, croppedInputPhoto.shape[1]):
			colorOfPixel = croppedInputPhoto[i, j]
			blue = colorOfPixel[0] + 0.0;
			green = colorOfPixel[1] + 0.0;
			red = colorOfPixel[2] + 0.0;

			if blue == 0.0:
				blue = 1
			if green == 0.0:
				green = 1
			if red > 80 and green < 90 and blue < 100:
				croppedInputPhoto[i, j] = [255, 255, 255]
			else: #else, make it black
				croppedInputPhoto[i, j] = [0, 0, 0]

	#%--------------------DETECT BLOBS--------------------%
	gray_img = cv2.cvtColor(croppedInputPhoto, cv2.COLOR_BGR2GRAY)

	img, contours, _ = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	if len(contours) > 0:
		numberOfContours = len(contours)
		largestArea = 0
		bestContour = -1
		for i in range(0, numberOfContours):
		    area = cv2.contourArea(contours[i], False)
		    if area > 700/3:
		    	x,y,w,h = cv2.boundingRect(contours[i])
		    	if float(w) / float(h) > 0.8 and float(w) / float(h) < 1.2 and float(h) / float(w) > 0.8 and float(h) / float(w) < 1.2:
			    	if area > largestArea:
				        largestArea = area
				        bestContour = i

		if bestContour >= 0:
		    global triggerFound
                    triggerFound = True
                    print "Stop sign found"
                    cv2.drawContours(croppedInputPhoto, contours, bestContour, (0,255,0), 2) #DEBUG
        cv2.imshow('stop sign contours', croppedInputPhoto) #DEBUG
        cv2.waitKey(30) #DEBUG



def detectCrosswalkSign(resizedInputPhoto):
    print "Detect crosswalk sign start"
    threeFourthsDown = resizedInputPhoto.shape[0] * (3.0 / 4)
    croppedInputPhoto = resizedInputPhoto[0:threeFourthsDown, :]
    for i in range(0, croppedInputPhoto.shape[0]):
		for j in range(0, croppedInputPhoto.shape[1]):
			colorOfPixel = croppedInputPhoto[i, j]
			blue = colorOfPixel[0] + 0.0;
			green = colorOfPixel[1] + 0.0;
			red = colorOfPixel[2] + 0.0;

			if blue == 0.0:
				blue = 1
			if green == 0.0:
				green = 1
			if red == 0.0:
				red = 1			
			if red < 210 and red > 100 and green < 210 and green > 90 and blue < 100:
				croppedInputPhoto[i, j] = [255, 255, 255]
			else: #else, make it black
                                #print "making this pixel black"
				croppedInputPhoto[i, j] = [0, 0, 0]

	#%--------------------DETECT BLOBS--------------------%
    gray_img = cv2.cvtColor(croppedInputPhoto, cv2.COLOR_BGR2GRAY)
    img, contours, _ = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        numberOfContours = len(contours)
        area = cv2.contourArea(contours[0], False)
        largestArea = 0
        bestContour = -1
        for i in range(0, numberOfContours):
            area = cv2.contourArea(contours[i], False)
            if area > 2000:
                x,y,w,h = cv2.boundingRect(contours[i])
                if float(w) / float(h) > 0.4 and float(w) / float(h) < 1.6 and float(h) / float(w) > 0.4 and float(h) / float(w) < 1.6:
                        if area > largestArea:
                                largestArea = area
                                bestContour = i


        if bestContour >= 0:
            global triggerFound
            triggerFound = True
            print "Crosswalk lines found"
            cv2.drawContours(croppedInputPhoto, contours, bestContour, (0,255,0), 2) #DEBUG
    cv2.imshow('crosswalk sign contours', croppedInputPhoto) #DEBUG
    cv2.waitKey(30) #DEBUG


def detectRoad(resizedInputPhoto):
    print "Detect road start"
    croppedInputPhoto = resizedInputPhoto[len(resizedInputPhoto)/2:len(resizedInputPhoto), :]
    croppedInputPhoto = croppedInputPhoto[0:len(croppedInputPhoto)/2, :]

    PIXEL_VARIANCE_THRESHOLD = 10.0
    AREA_THRESHOLD_PERCENTAGE = 0.6
    thresholdImage =  cv2.cvtColor(croppedInputPhoto, cv2.COLOR_BGR2GRAY)
    for i in range(0,len(croppedInputPhoto)-1):
           for j in range(0,len(croppedInputPhoto[0])-1):
              if np.var(croppedInputPhoto[i][j]) < PIXEL_VARIANCE_THRESHOLD:
                 thresholdImage[i][j] = 255
           else:
                  thresholdImage[i][j] = 0

    #detect blobs
    img, contours, _ = cv2.findContours(thresholdImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    numberOfContours = len(contours)
    areaThreshold = len(croppedInputPhoto) * len(croppedInputPhoto[0]) * AREA_THRESHOLD_PERCENTAGE

    largestArea = 0
    largestContour = 0
    for i in range(0, numberOfContours):
            area = cv2.contourArea(contours[i], False)
    if area > largestArea:
        largestArea = area
        largestContour = i

    roadBlobDetected = False
    if largestArea > areaThreshold:
            global triggerFound
            triggerFound = True
            print "Detect road found"
    cv2.imshow('Road Contours', croppedInputPhoto) #DEBUG
    cv2.waitKey(30) #DEBUG


#%--------------------READ IMAGE--------------------%

#camera = picamera.PiCamera()
vibration_motor = 8
buzzer_motor = 7

#camera.preview_fullscreen=False
#camera.preview_window=(320, 320, 640, 480)
#camera.start_preview()
# sleep(5)

while True:
    #choice = input("Press the following keys for feature detection algorithms: \n1: Stop Sign\n2: Crosswalk Sign\n3: Crosswalk Lines\n4: Road\n5: Traffic Lights")

    #reset USB ports
    
    os.system("sudo ./usbreset /dev/bus/usb/001/" + os.popen("lsusb | grep 'C270' | grep -o 'Device....' | grep -o '...$'").read())
    os.system("fswebcam input.jpg -r 1280x720")        
    inputPhoto = cv2.imread('input.jpg')

    
    #%--------------------RESIZE IMAGE--------------------%
    #make longest edge 400

    #get dimensions of image
    height, width, channels = inputPhoto.shape
    #print height, width

    if height > width:
    	translationFactor = 100.0 / height
    else:
    	translationFactor = 100.0 / width
    #print translationFactor


    #resize the image so the longest edge is 1200 pixels, keeping the same aspect ratio
    resizedInputPhoto = cv2.resize(inputPhoto,None,fx=translationFactor, fy=translationFactor, interpolation = cv2.INTER_CUBIC)
    print "start parallel"

    #%--------------CALL THE PROCESSES IN PARALLEL-----------------%
    #declare thread objects

    #thread.start_new_thread(detectStopSign, {resizedInputPhoto})
    #thread.start_new_thread(detectCrosswalkSign, (resizedInputPhoto))
    #thread.start_new_thread(detectRoad, (resizedInputPhoto))
    #crossWalkLineThread = detectCrosswalkLines(resizedInputPhoto)

    
    stopSignThread = Thread(target = detectStopSign, args = (resizedInputPhoto,) )
    crosswalkSignThread = Thread(target = detectCrosswalkSign, args = (resizedInputPhoto,) )
    detectRoadThread = Thread(target = detectRoad, args = (resizedInputPhoto,) )
    

    #start all threads
    stopSignThread.start()
    crosswalkSignThread.start()
    detectRoadThread.start()
    #crossWalkLineThread.start()

    #keep track of threads w list
    threads = []
    threads.append(stopSignThread)
    threads.append(crosswalkSignThread)
    threads.append(detectRoadThread)
    #threads.append(crossWalkLineThread)

    #wait for all to complete
    for t in threads:
        t.join()

    
    #make sure ports aren't already in use
    grovepi.digitalWrite(7,0)
    grovepi.digitalWrite(8,0)
    
    if triggerFound:
        triggerFound = False
        grovepi.digitalWrite(vibration_motor,1)
        #spend 3 seconds making 3 beeps
        for i in range(1,3):
                            grovepi.digitalWrite(buzzer_motor,1)
                            time.sleep(0.2)
                            grovepi.digitalWrite(buzzer_motor,0)
                            time.sleep(0.2)
        #end vibration
        grovepi.digitalWrite(vibration_motor,0)
    else:
        print "NOTHING FOUND"

    cv2.waitKey(0)

    
