import thread
#import picamera
import cv2
import numpy as np
import time
#import grovepi
import heapq
import os
from time import sleep

translationFactorAmount = 400.0


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
                                time.sleep(0.5)
                                grovepi.digitalWrite(buzzer_motor,0)
                                time.sleep(0.5)
	        #end vibration
	        grovepi.digitalWrite(vibration_motor,0)
	        cv2.drawContours(croppedInputPhoto, contours, bestContour, (0,255,0), 2) #DEBUG
        	cv2.imshow('contours', croppedInputPhoto) #DEBUG
        	cv2.waitKey(3000) #DEBUG
        	print "STOP SIGN DONE"



def detectCrosswalkSign(resizedInputPhoto):
    print "CROSSWALK SIGN START"
    cv2.imshow('image', resizedInputPhoto)
    cv2.waitKey(3000)
    threeFourthsDown = resizedInputPhoto.shape[0] * (3.0 / 4)
    croppedInputPhoto = resizedInputPhoto[0:threeFourthsDown, :]
    cv2.imshow('image', croppedInputPhoto)
    cv2.waitKey(3000)
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
    print "about to detect blobs"
    gray_img = cv2.cvtColor(croppedInputPhoto, cv2.COLOR_BGR2GRAY)
    img, contours, _ = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        print "found " + str(len(contours))+" contours"
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
                        time.sleep(0.5)
                        grovepi.digitalWrite(buzzer_motor,0)
                        time.sleep(0.5)
        #end vibration
        grovepi.digitalWrite(vibration_motor,0)
        grovepi.digitalWrite(7,0)
        cv2.drawContours(croppedInputPhoto, contours, bestContour, (0,255,0), 2) #DEBUG
        cv2.imshow('contours', croppedInputPhoto) #DEBUG
        cv2.waitKey(3000) #DEBUG
        print "CROSSWALK SIGN DONE"





listOfAlreadyProcessedFiles = []

#%--------------------READ IMAGE--------------------%

#camera.preview_fullscreen=False
#camera.preview_window=(320, 320, 640, 480)
#camera.start_preview()

while True:
    for fileName in os.listdir('/Users/Diego/Pictures/Photo Booth Library/Pictures/'):
        #if file is a jpg and not in our list
        if (fileName[-4:] == '.jpg' or fileName[-4:] == '.JPG') and fileName not in listOfAlreadyProcessedFiles:
            #add it to already processed list
            listOfAlreadyProcessedFiles.append(fileName)
   
            inputPhoto = cv2.imread('/Users/Diego/Pictures/Photo Booth Library/Pictures/' + fileName)

    
            #%--------------------RESIZE IMAGE--------------------%
            #make longest edge 400

            #get dimensions of image
            height, width, channels = inputPhoto.shape
            #print height, width

            if height > width:
            	translationFactor = translationFactorAmount / height
            else:
            	translationFactor = translationFactorAmount / width
            #print translationFactor


            #resize the image so the longest edge is 1200 pixels, keeping the same aspect ratio
            resizedInputPhoto = cv2.resize(inputPhoto,None,fx=translationFactor, fy=translationFactor, interpolation = cv2.INTER_CUBIC)
            cv2.imshow('image', resizedInputPhoto)
            cv2.waitKey(10)

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
            #thread.start_new_thread(detectStopSign, (resizedInputPhoto,))
            #thread.start_new_thread(detectCrosswalkSign, (resizedInputPhoto,))
            #thread.start_new_thread(detectRoad, (resizedInputPhoto,))
            
            print "cool choice bro. You picked choice " + str(choice)
            grovepi.digitalWrite(7,0)
            grovepi.digitalWrite(8,0)
            
            if choice == 1:
                detectStopSign(resizedInputPhoto)
            elif choice == 2:
                detectCrosswalkSign(resizedInputPhoto)
            elif choice == 3:
                detectCrosswalkLines(resizedInputPhoto)
                print "waiting"
            elif choice == 4:
                detectRoad(resizedInputPhoto)
    
