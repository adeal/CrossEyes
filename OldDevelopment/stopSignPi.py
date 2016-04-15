import numpy as np
import cv2
import grovepi
import picamera
import time


#diego
#%--------------------READ IMAGE--------------------%

camera = picamera.PiCamera()
vibration_motor = 5
buzzer_motor = 6

while True:
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
        threeFourthsDown = resizedInputPhoto.shape[0] * (3.0 / 4)
        # print inputPhoto.shape[0]
        # print resizedInputPhoto.shape[0]
        # print threeFourthsDown
        croppedInputPhoto = resizedInputPhoto[0:threeFourthsDown, :]
        cv2.imshow('image', croppedInputPhoto)
        cv2.waitKey(10)


	#%--------------------THRESHOLD IMAGE--------------------%

	#go through each pixel
	for i in range(0, croppedInputPhoto.shape[0]):
		for j in range(0, croppedInputPhoto.shape[1]):
			#look at the pixel
			colorOfPixel = croppedInputPhoto[i, j]
			blue = colorOfPixel[0] + 0.0;
			green = colorOfPixel[1] + 0.0;
			red = colorOfPixel[2] + 0.0;
			#print blue, green, red

			#make sure we get no divide by zero errors
			if blue == 0.0:
				blue = 1
			if green == 0.0:
				green = 1
				
			#if pixel is red enough, make it white
			#was 1.1
			if red > 50 and green < 70 and blue < 70:
				croppedInputPhoto[i, j] = [255, 255, 255]
			else: #else, make it black
				croppedInputPhoto[i, j] = [0, 0, 0]


	biggerYetBlurrierThresholdedImageForViewing = cv2.resize(croppedInputPhoto,None,fx=(1 / translationFactor), fy=(1 / translationFactor), interpolation = cv2.INTER_CUBIC)
	height, width, channels = biggerYetBlurrierThresholdedImageForViewing.shape
	# print height, width
	# print translationFactor
	# print 1 / translationFactor
	#cv2.imwrite( "CVOutput/thresholdedImage" + fn, croppedInputPhoto)
	cv2.imshow('image', biggerYetBlurrierThresholdedImageForViewing)
	cv2.waitKey(10)		


        #austin
        #for this part, use the Thresholded_Images
        #%--------------------DETECT BLOBS--------------------%
        # blobMeasurement = cv2.findContours(croppedInputPhoto, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # numberOfBlobs = len(blobMeasurement)
        # print numberOfBlobs
	gray_img = cv2.cvtColor(croppedInputPhoto, cv2.COLOR_BGR2GRAY)
	cv2.imshow('gray_img', gray_img)
	cv2.waitKey(10)

	img, contours, _ = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# if fn == "stop6.jpg" or fn == "stop7.jpg" or fn == "stop8.jpg":
	# 	cv2.imshow('img', img)
	# 	cv2.waitKey(0)

		
	if len(contours) > 0:
		numberOfContours = len(contours)
		largestArea = 0
		bestContour = -1
		for i in range(0, numberOfContours):
		    area = cv2.contourArea(contours[i], False)
		    # print "area of this contour is " + str(area)
	      	#make sure the contour is large enough to even bother with
		    if area > 700:
		    	#make sure the contour is square enough
		    	x,y,w,h = cv2.boundingRect(contours[i])
		    	print float(w) / float(h)
		    	print float(h) / float(w)
        	    	if float(w) / float(h) > 0.8 and float(w) / float(h) < 1.2 and float(h) / float(w) > 0.8 and float(h) / float(w) < 1.2:
			    	if area > largestArea:
				        largestArea = area
				        bestContour = i
				        
		print "largestArea in pic is " + str(largestArea)
		if bestContour >= 0:
			cv2.drawContours(resizedInputPhoto, contours, bestContour, (0,255,0), 3)
			print "found stopsign in image"
			cv2.imshow('contours', resizedInputPhoto)
			cv2.waitKey(10)
		else:
			print "found contours, but none that looked like a stopsign in image"

	else:
		print "No contours found in this image"


	# thresholdedInputPhoto = []
	# width, height = thresholdedInputPhoto.shape
	# for i in range(0, width):
	#     for j in range(0, height):
	#         if thresholdedInputPhoto.item(i, j, 2) / thresholdedInputPhoto.item(i, j, 1) + thresholdedInputPhoto.item(i, j, 3) < 1:
	#             thresholdedInputPhoto.itemset((i, j), 0)

	# # http://stackoverflow.com/questions/12995937/count-all-values-in-a-matrix-greater-than-a-value
	# thresholdedInputPhoto[np.where(thresholdedInputPhoto > 0)] = 0


	# 	#%------------TELL PI TO VIBRATE---------------%#
	if bestContour >= 0:
	# if largestArea > 1800:
                #vibrate entire duration
		grovepi.digitalWrite(vibration_motor,1)
		#spend 3 seconds making 3 beeps
		for i in range(1,3):
                        grovepi.digitalWrite(buzzer_motor,1)
                        time.sleep(0.5)
                        grovepi.digitalWrite(buzzer_motor,0)
                #end vibration
                grovepi.digitalWrite(vibration_motor,0)
