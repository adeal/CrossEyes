import thread
import picamera
import cv2
import numpy as np
import time
import grovepi
import heapq





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
    # print threeFourthsDown
    croppedInputPhoto = resizedInputPhoto[height / 2:height, :]
    cv2.imshow('image', croppedInputPhoto)
    cv2.waitKey(0)

    gray_img = cv2.cvtColor(croppedInputPhoto, cv2.COLOR_BGR2GRAY)
    ret, gray_img = cv2.threshold(gray_img, 150, 255, cv2.THRESH_BINARY)
    cv2.imshow('thresholded', gray_img)
    cv2.waitKey(0)

    img, contours, _ = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('img', img)
    cv2.waitKey(0)

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
        print "CROSSWALK DETECTED"
        for contour in crossLineContourIndexes:
            cv2.drawContours(croppedInputPhoto, contours, contour, (0,255,0), 3)

    cv2.imshow('FINAL IMAGE', croppedInputPhoto)
    cv2.waitKey(3000)



#functions
def detectStopSign(resizedInputPhoto):
        print "STOP SIGN START"
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
			if red > 50 and green < 70 and blue < 70:
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
		    if area > 700:
		    	x,y,w,h = cv2.boundingRect(contours[i])
		    	print float(w) / float(h)
		    	print float(h) / float(w)
		    	if float(w) / float(h) > 0.8 and float(w) / float(h) < 1.2 and float(h) / float(w) > 0.8 and float(h) / float(w) < 1.2:
			    	if area > largestArea:
				        largestArea = area
				        bestContour = i

		if bestContour >= 0:
			grovepi.digitalWrite(vibration_motor,1)
			#spend 3 seconds making 3 beeps
			for i in range(1,3):
                                grovepi.digitalWrite(buzzer_motor,1)
                                time.sleep(0.2)
                                grovepi.digitalWrite(buzzer_motor,0)
                                time.sleep(0.2)
	        #end vibration
	        grovepi.digitalWrite(vibration_motor,0)
	        cv2.drawContours(croppedInputPhoto, contours, bestContour, (0,255,0), 2) #DEBUG
        	cv2.imshow('contours', croppedInputPhoto) #DEBUG
        	cv2.waitKey(3000) #DEBUG
        	print "STOP SIGN DONE"



def detectCrosswalkSign(resizedInputPhoto):
    print "CROSSWALK SIGN START"
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
			if red > 230 and green < 100 and blue < 100:
				croppedInputPhoto[i, j] = [255, 255, 255]
			else: #else, make it black
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
			grovepi.digitalWrite(vibration_motor,1)
			#spend 3 seconds making 3 beeps
			for i in range(1,3):
                                grovepi.digitalWrite(buzzer_motor,1)
                                time.sleep(0.2)
                                grovepi.digitalWrite(buzzer_motor,0)
                                time.sleep(0.2)
	        #end vibration
	        grovepi.digitalWrite(vibration_motor,0)
	        cv2.drawContours(croppedInputPhoto, contours, bestContour, (0,255,0), 2) #DEBUG
        	cv2.imshow('contours', croppedInputPhoto) #DEBUG
        	cv2.waitKey(3000) #DEBUG
        	print "CROSSWALK SIGN DONE"




def detectRoad(resizedInputPhoto):
    print "DETECT ROAD START"
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
    if numberOfContours > 0: #DEBUG
            cv2.drawContours(croppedInputPhoto, contours, largestContour, (0,255,0), 2) #DEBUG
            cv2.imshow('Road Contours', croppedInputPhoto) #DEBUG
            cv2.waitKey(3000) #DEBUG

    #make decision

    roadBlobDetected = False
    if largestArea > areaThreshold:
            print "ROAD DETECTED" #DEBUG
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
            print "NO ROAD DETECTED" #DEBUG
            #ret false
    print "ROAD DONE"


#%--------------------READ IMAGE--------------------%

camera = picamera.PiCamera()
vibration_motor = 8
buzzer_motor = 7

while True:
    choice = input("Press the following keys for feature detection algorithms: \n1: Stop Sign\n2: Crosswalk Sign\n3: Crosswalk Lines\n4: Road\n5: Traffic Lights")

    camera.capture('input.jpg')
    inputPhoto = cv2.imread('input.jpg')
    #cv2.imshow('image', inputPhoto)
    #cv2.waitKey(10)

    
    #%--------------------RESIZE IMAGE--------------------%
    #make longest edge 400

    #get dimensions of image
    height, width, channels = inputPhoto.shape
    #print height, width

    if height > width:
    	translationFactor = 400.0 / height
    else:
    	translationFactor = 400.0 / width
    #print translationFactor

    #resize the image so the longest edge is 1200 pixels, keeping the same aspect ratio
    resizedInputPhoto = cv2.resize(inputPhoto,None,fx=translationFactor, fy=translationFactor, interpolation = cv2.INTER_CUBIC)
    cv2.imshow('image', resizedInputPhoto)
    cv2.waitKey(10)

    #crop the bottom 4th of the image
    #threeFourthsDown = resizedInputPhoto.shape[0] * (3.0 / 4)
    # print inputPhoto.shape[0]
    # print resizedInputPhoto.shape[0]
    # print threeFourthsDown
    #croppedInputPhoto = resizedInputPhoto[0:threeFourthsDown, :]
    # cv2.imshow('image', croppedInputPhoto)
    # cv2.waitKey(0)


    #%--------------CALL THE PROCESSES IN PARALLEL-----------------%
    #declare thread objects
    #stopSignThread = detectStopSign(resizedInputPhoto)
    #crosswalkSignThread = detectCrosswalkSign(resizedInputPhoto)
    #detectRoadThread = detectRoad(resizedInputPhoto)

    #start all threads
    #stopSignThread.start()
    #crosswalkSignThread.start()
    #detectRoadThread.start()

    #keep track of threads w list
    #threads = []
    #threads.append(stopSignThread)
    #threads.append(crosswalkSignThread)
    #threads.append(detectRoadThread)

    #wait for all to complete
    ##for t in threads:
    #    t.join()

    #basic multithreading
    print "Taking picture and calling threads"
    
    #args = []
    #args.append(resizedInputPhoto)
    thread.start_new_thread(detectStopSign, (resizedInputPhoto,))
    thread.start_new_thread(detectCrosswalkSign, (resizedInputPhoto,))
    thread.start_new_thread(detectRoad, (resizedInputPhoto,))

    print "Wait until all detectors are completed. Press key 0 to continue"
    cv2.waitKey(0)

    if choice == 1:
        detectStopSign(resizedInputPhoto)
    elif choice == 2:
        detectCrosswalkSign(resizedInputPhoto)
    elif choice == 3:
        #detectCrosswalkLines(resizedInputPhoto)
        print "waiting"
    elif choice == 4:
        detectRoad(resizedInputPhoto)




