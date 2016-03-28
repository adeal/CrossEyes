from threading import Thread
import cv2
import numpy as np
import time
import grovepi
import heapq
import os
from time import sleep

#global variables
stopTriggerFound = False
crossTriggerFound = False
vibration_motor = 8
buzzer_motor = 7
imageEdge = 100.0

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
			if red / (blue + green) > 0.75:
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
		    if area > 700/(imageEdge/400): #original error measured w.r.t. 400
		    	x,y,w,h = cv2.boundingRect(contours[i])
		    	#print float(w) / float(h)
		    	#print float(h) / float(w)
		    	if float(w) / float(h) > 0.8 and float(w) / float(h) < 1.2 and float(h) / float(w) > 0.8 and float(h) / float(w) < 1.2:
			    	if area > largestArea:
				        largestArea = area
				        bestContour = i

		if bestContour >= 0:
		    print "STOP SIGN DETECTED"
                    global stopTriggerFound
                    stopTriggerFound = True
                else:
                    print "NO STOP SIGN FOUND"
                    global stopTriggerFound
                    stopTriggerFound = False
	        #cv2.drawContours(croppedInputPhoto, contours, bestContour, (0,255,0), 2) #DEBUG
        	#cv2.imshow('contours', croppedInputPhoto) #DEBUG
        	#cv2.waitKey(3000) #DEBUG
        print "STOP SIGN DONE"



def detectCrosswalkSign(resizedInputPhoto):
    print "CROSSWALK SIGN START"
    #cv2.imshow('image', resizedInputPhoto)
    #cv2.waitKey(3000)
    threeFourthsDown = resizedInputPhoto.shape[0] * (3.0 / 4)
    croppedInputPhoto = resizedInputPhoto[0:threeFourthsDown, :]
    #cv2.imshow('image', croppedInputPhoto)
    #cv2.waitKey(3000)
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
	    #print "making this pixel white"
	    else: #else, make it black
                #print "making this pixel black"
		croppedInputPhoto[i, j] = [0, 0, 0]

	#%--------------------DETECT BLOBS--------------------%
    #print "about to detect blobs"
    gray_img = cv2.cvtColor(croppedInputPhoto, cv2.COLOR_BGR2GRAY)
    img, contours, _ = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        #print "found " + str(len(contours))+" contours"
        numberOfContours = len(contours)
        area = cv2.contourArea(contours[0], False)
        largestArea = 0
        bestContour = -1
        for i in range(0, numberOfContours):
            area = cv2.contourArea(contours[i], False)
            if area > 2000/(imageEdge/400): #original area measured w.r.t. 400
                x,y,w,h = cv2.boundingRect(contours[i])
                if float(w) / float(h) > 0.4 and float(w) / float(h) < 1.6 and float(h) / float(w) > 0.4 and float(h) / float(w) < 1.6:
                    if area > largestArea:
                        largestArea = area
                        bestContour = i
                        
        if bestContour >= 0:
            print "CROSSWALK SIGN DETECTED"
            global crossTriggerFound
            crossTriggerFound = True
        else:
            print "NO CROSSWALK SIGN FOUND"
            global crossTriggerFound
            crossTriggerFound = False
        #end vibration
        #grovepi.digitalWrite(vibration_motor,0)
        #grovepi.digitalWrite(7,0)
        #cv2.drawContours(croppedInputPhoto, contours, bestContour, (0,255,0), 2) #DEBUG
        #cv2.imshow('contours', croppedInputPhoto) #DEBUG
        #cv2.waitKey(3000) #DEBUG
        
    print "CROSSWALK SIGN DONE"

def sendStopAlertSignal():
    global stopTriggerFound
    stopTriggerFound = False
    grovepi.digitalWrite(vibration_motor,1)
    #spend 3 seconds making 1 long beep
    grovepi.digitalWrite(buzzer_motor,1)
    time.sleep(3)
    grovepi.digitalWrite(buzzer_motor,0)
    grovepi.digitalWrite(vibration_motor,0)

def sendCrossAlertSignal():
    global crossTriggerFound
    crossTriggerFound = False
    grovepi.digitalWrite(vibration_motor,1)
    #spend 3 seconds making 3 beeps
    for i in range(1,3):
        grovepi.digitalWrite(buzzer_motor,1)
        time.sleep(0.4)
        grovepi.digitalWrite(buzzer_motor,0)
        time.sleep(0.3)
    #end vibration
    grovepi.digitalWrite(vibration_motor,0)

def sendBothAlertSignal():
    global stopTriggerFound
    stopTriggerFound = False
    global crossTriggerFound
    crossTriggerFound = False
    grovepi.digitalWrite(vibration_motor,1)
    #spend 3 second making 1 long beep, then 3 seconds making 3 beeps
    grovepi.digitalWrite(buzzer_motor,1)
    time.sleep(3)
    grovepi.digitalWrite(buzzer_motor,0)
    for i in range(1,3):
        grovepi.digitalWrite(buzzer_motor,1)
        time.sleep(0.4)
        grovepi.digitalWrite(buzzer_motor,0)
        time.sleep(0.3)
    #end vibration
    grovepi.digitalWrite(vibration_motor,0)

#Code Start
#alertThread = Thread(target = sendAlertSignal, args = ())
#%--------------------READ IMAGE--------------------%
# while True:
#     choice = input("Press the following keys for feature detection algorithms: \n1: Stop Sign\n2: Crosswalk Sign\n3: Crosswalk Lines\n4: Road\n5: Traffic Lights")

#     #reset USB ports
#     os.system("sudo ./usbreset /dev/bus/usb/001/" + os.popen("lsusb | grep 'C270' | grep -o 'Device....' | grep -o '...$'").read())
#     os.system("fswebcam input.jpg -r 1280x720")        
#     inputPhoto = cv2.imread('input.jpg')
#for fn in os.listdir('linesOnly'):
#    if fn[-4:] == '.jpg':
firstRun = True
#sleep(15)
for i in range(1,3):
    grovepi.digitalWrite(buzzer_motor,1)
    time.sleep(0.3)
    grovepi.digitalWrite(buzzer_motor,0)
    time.sleep(0.3)
    grovepi.digitalWrite(buzzer_motor,1)
    time.sleep(0.3)
    grovepi.digitalWrite(buzzer_motor,0)
    time.sleep(0.3)
    grovepi.digitalWrite(buzzer_motor,1)
    time.sleep(0.3)
    grovepi.digitalWrite(buzzer_motor,0)
os.chdir("/home/pi/CrossEyes")
currentPic = 1
while True:
    os.system("sudo ./usbreset /dev/bus/usb/001/" + os.popen("lsusb | grep 'C270' | grep -o 'Device....' | grep -o '...$'").read())
    os.system("fswebcam input.jpg -r 1280x720")
    inputPhoto = cv2.imread('input.jpg')
    if firstRun or ~(inputPhoto == lastInputPhoto).all():
    
        #%--------------------RESIZE IMAGE--------------------%
        #make longest edge the size of recorded imageEdge global variable

        #get dimensions of image
        height, width, channels = inputPhoto.shape
        #print height, width

        if height > width:
            translationFactor = imageEdge / height
        else:
            translationFactor = imageEdge / width
        #print translationFactor

        #resize the image so the longest edge is 1200 pixels, keeping the same aspect ratio
        resizedInputPhoto = cv2.resize(inputPhoto,None,fx=translationFactor, fy=translationFactor, interpolation = cv2.INTER_CUBIC)
        
        stopSignThread = Thread(target = detectStopSign, args = (resizedInputPhoto,) )
        crosswalkSignThread = Thread(target = detectCrosswalkSign, args = (resizedInputPhoto,) )

        #start all threads
        stopSignThread.start()
        crosswalkSignThread.start()

        #wait for all threads to finish
        stopSignThread.join()
        crosswalkSignThread.join()
        
        if stopTriggerFound and ~crossTriggerFound:
            print "stopTriggerFound == True, sending STOP alert signal!"
            sendStopAlertSignal()
        elif ~stopTriggerFound and crossTriggerFound:
            print "stopCrossFound == True, sending CROSS alert signal!"
            sendCrossAlertSignal()
        elif stopTriggerFound and crossTriggerFound:
            print "stopTriggerFound == True AND stopCrossTriggerFound == True, sending BOTH alert signal!"
            sendBothAlertSignal()
            if currentPic < 1000:
                cv2.imwrite("/home/pi/CrossEyes/crosseyesSignLog/positivePhoto_" + str(currentPic) + ".jpg", inputPhoto)
                currentPic = currentPic + 1
            #if the last alert is running, wait for it to finish
            #try:
            #    alertThread.start()
            #    alertThread.join()
            #except:
                #send the new alert
            #    alertThread.join()
            #    alertThread.start()
            #    alertThread.join()
        else:
            print "NOTHING FOUND"
        lastInputPhoto = inputPhoto
        firstRun = False
        
