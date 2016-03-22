#listOfDetectionFiles
import numpy as np
import cv2
import grovepi
import picamera
import time


def detectStopSign(croppedInputPhoto):
	#%--------------------THRESHOLD IMAGE--------------------%

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



def detectCrosswalkSign(croppedInputPhoto):
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




def detectRoad(croppedInputPhoto):
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
        cv2.imshow('contours', croppedInputPhoto) #DEBUG
        cv2.waitKey(3000) #DEBUG

    #make decision

    roadBlobDetected = False
    if largestArea > areaThreshold:
        print fn + " = ROAD DETECTED" #DEBUG
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
        print fn + " = NO ROAD" #DEBUG
        #ret false
