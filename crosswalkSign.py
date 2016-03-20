import numpy as np
import cv2
#import grovepi


#diego
#%--------------------READ IMAGE--------------------%

import os
whichPicWeAt = 0
for fn in os.listdir('CrossWalkSignInput'):
	if fn[-4:] == '.jpg':
		whichPicWeAt += 1
		inputPhoto = cv2.imread('CrossWalkSignInput/' + fn)
#inputPhoto = cv2.imread('CVInput/stop.jpg')

# cv2.imshow('image', inputPhoto)
# cv2.waitKey(0)


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
		# cv2.imshow('image', resizedInputPhoto)
		# cv2.waitKey(0)

		#crop the bottom 4th of the image
		threeFourthsDown = resizedInputPhoto.shape[0] * (3.0 / 4)
		# print inputPhoto.shape[0]
		# print resizedInputPhoto.shape[0]
		#print threeFourthsDown
		croppedInputPhoto = resizedInputPhoto[0:threeFourthsDown, :]
		# cv2.imshow('image', croppedInputPhoto)
		# cv2.waitKey(0)


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
				if red == 0.0:
					red = 1

				#if pixel is yellow enough, make it white
				
				if red > 230 and green > 180 and green < 224 and blue < 15:
					croppedInputPhoto[i, j] = [255, 255, 255]
				else: #else, make it black
					croppedInputPhoto[i, j] = [0, 0, 0]


		biggerYetBlurrierThresholdedImageForViewing = cv2.resize(croppedInputPhoto,None,fx=(1 / translationFactor), fy=(1 / translationFactor), interpolation = cv2.INTER_CUBIC)
		height, width, channels = biggerYetBlurrierThresholdedImageForViewing.shape
		# print height, width
		# print translationFactor
		# print 1 / translationFactor
		stringWhichPicWeAt = str(whichPicWeAt)
		cv2.imwrite( "CrossWalkSignOutput/thresholdedImage" + stringWhichPicWeAt + ".jpg", croppedInputPhoto)
	# cv2.imshow('image', biggerYetBlurrierThresholdedImageForViewing)
	# cv2.waitKey(0)		


#austin
#for this part, use the Thresholded_Images
#%--------------------DETECT BLOBS--------------------%
# blobMeasurement = cv2.findContours(croppedInputPhoto, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# numberOfBlobs = len(blobMeasurement)
# print numberOfBlobs
		gray_img = cv2.cvtColor(croppedInputPhoto, cv2.COLOR_BGR2GRAY)
		# cv2.imshow('gray_img', gray_img)
		# cv2.waitKey(0)

		img, contours, _ = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		# cv2.imshow('img', img)
		# cv2.waitKey(0)


		#don't error if there aren't any contours
		if len(contours) > 0:
			numberOfContours = len(contours)
			area = cv2.contourArea(contours[0], False)
			# print area

			largestArea = 0
			largestContour = 0
			for i in range(0, numberOfContours):
			    area = cv2.contourArea(contours[i], False)
			    if area > largestArea:
			        largestArea = area
			        largestContour = i

			cv2.drawContours(resizedInputPhoto, contours, largestContour, (0,255,0), 3)
			cv2.imshow('contours', resizedInputPhoto)

			cv2.waitKey(0)
		else:
			print "No contours found in this image"
			print fn


		# thresholdedInputPhoto = []
		# width, height = thresholdedInputPhoto.shape
		# for i in range(0, width):
		#     for j in range(0, height):
		#         if thresholdedInputPhoto.item(i, j, 2) / thresholdedInputPhoto.item(i, j, 1) + thresholdedInputPhoto.item(i, j, 3) < 1:
		#             thresholdedInputPhoto.itemset((i, j), 0)

		# # http://stackoverflow.com/questions/12995937/count-all-values-in-a-matrix-greater-than-a-value
		# thresholdedInputPhoto[np.where(thresholdedInputPhoto > 0)] = 0


		# 	#%------------TELL PI TO VIBRATE---------------%#
		# if largestArea > 1800:
		# 	grovepi.digitalWrite(vibration_motor,3)

