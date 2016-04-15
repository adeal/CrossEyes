__author__ = 'XL'

import numpy as np
import cv2
import os

#if speed issues are encountered, consider reducing the size of the cropped image and increasing the area percentage
AREA_THRESHOLD_PERCENTAGE = 0.4 #suggested vals 0.5-1
PIXEL_VARIANCE_THRESHOLD = 20 #suggested vals 0-100
LONGEST_RESIZED_EDGE = 400 #suggested vals dependent on computation time

whichPicWeAt = 0
for fn in os.listdir('roadFiles'):
	if fn[-4:] == '.jpg':
		inputPhoto = cv2.imread('roadFiles/' + fn)
		print "Current Image: " + fn
        # cv2.imshow("image", inputPhoto)
        # cv2.waitKey(0)
        height, width, channels = inputPhoto.shape
        if height > width:
            translationFactor = float(LONGEST_RESIZED_EDGE) / height
        else:
            translationFactor = float(LONGEST_RESIZED_EDGE) / width

        #resize
        resizedInputPhoto = cv2.resize(inputPhoto,None,fx=translationFactor, fy=translationFactor, interpolation = cv2.INTER_CUBIC)
        cv2.imshow('resized image', resizedInputPhoto) #DEBUG
        cv2.waitKey(0) #DEBUG

        #crop
        #take off the top half
        croppedInputPhoto = resizedInputPhoto[len(resizedInputPhoto)/2:len(resizedInputPhoto), :]
        #take off the bottom 1/4th = 1/2th of the already cropped photo
        croppedInputPhoto = croppedInputPhoto[0:len(croppedInputPhoto)/2, :]
        cv2.imshow('cropped image', croppedInputPhoto) #DEBUG
        cv2.waitKey(0) #DEBUG

        #measure total variance: not currently included in the final calculation, but worth revisiting for efficiency
        # lowVariance = False;
        # threshold = 1;
        # var = np.var(croppedInputPhoto)
        # if var < threshold:
        #     lowVariance = True;
        # print str(lowVariance) + ": Variance = " + str(var) + " <= " + str(threshold)

        #threshold image
        #pixels below the pixel var threshold will be made white, all others become black
        #designed to keep all shades of white, black and gray (colors in roads), but remove any other color
        thresholdImage =  cv2.cvtColor(croppedInputPhoto, cv2.COLOR_BGR2GRAY)
        print str(len(croppedInputPhoto)) #DEBUG
        print str(len(croppedInputPhoto[0])) #DEBUG
        for i in range(0,len(croppedInputPhoto)-1):
            for j in range(0,len(croppedInputPhoto[0])-1):
                # print thresholdImage[j][i]
                if np.var(croppedInputPhoto[i][j]) < PIXEL_VARIANCE_THRESHOLD:
                    thresholdImage[i][j] = 255
                else:
                    thresholdImage[i][j] = 0
        cv2.imshow('threshold BW image', thresholdImage) #DEBUG
        cv2.waitKey(0) #DEBUG

        #detect blobs
        img, contours, _ = cv2.findContours(thresholdImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        numberOfContours = len(contours)
        print "Number of Contours = " + str(numberOfContours) #DEBUG

        #areaThreshold =  LONGEST_RESIZED_EDGE/4 * LONGEST_RESIZED_EDGE/2 * AREA_THRESHOLD_PERCENTAGE
        areaThreshold = len(croppedInputPhoto) * len(croppedInputPhoto[0]) * AREA_THRESHOLD_PERCENTAGE

        largestArea = 0
        largestContour = 0
        for i in range(0, numberOfContours):
            area = cv2.contourArea(contours[i], False)
            if area > largestArea:
                largestArea = area
                largestContour = i
            # cv2.drawContours(croppedInputPhoto, contours, i, (0,255,0), 2)
        if numberOfContours > 0: #DEBUG
            print "largest area = " + str(largestArea) + ", threshold area = " + str(areaThreshold) #DEBUG
            cv2.drawContours(croppedInputPhoto, contours, largestContour, (0,255,0), 2) #DEBUG
            cv2.imshow('contours', croppedInputPhoto) #DEBUG
            cv2.waitKey(0) #DEBUG
        else: #DEBUG
            print "No blobs detected" #DEBUG

        #detect lines
        # gray = cv2.cvtColor(croppedInputPhoto,cv2.COLOR_BGR2GRAY)
        # cv2.imshow('gray image', gray)
        # cv2.waitKey(0)
        # edges = cv2.Canny(gray,50,350)
        # cv2.imshow('edges in image', edges)
        # cv2.waitKey(0)
        # minLineLength = 500
        # maxLineGap = 1
        # numLongLines = 0
        # total = 0
        # lines = cv2.HoughLinesP(edges,1,np.pi/360,25,minLineLength,maxLineGap)
        # numLines = len(lines)
        # for i in range(numLines):
        #     if abs(lines[i][0][2] - lines[i][0][0]) >= 20: #x2-x1
        #         numLongLines += 1
        #         cv2.line(croppedInputPhoto,(lines[i][0][0],lines[i][0][1]),(lines[i][0][2],lines[i][0][3]),(0,255,0),1) #debug: x1, y1, x2, y2
        #     total += abs(lines[i][0][2] - lines[i][0][0])
        #     # cv2.line(croppedInputPhoto,(lines[i][0][0],lines[i][0][1]),(lines[i][0][2],lines[i][0][3]),(0,255,0),1) #debug: x1, y1, x2, y2
        # cv2.imshow('lines in image', croppedInputPhoto)
        # print "Number of lines found = " + str(len(lines))
        # print "Average line length = " + str(total/len(lines))
        # print "Number of long lines found = " + str(numLongLines)
        # cv2.waitKey(0)

        #make decision

        roadBlobDetected = False
        if largestArea > areaThreshold:
            print fn + " = ROAD DETECTED" #DEBUG
            #ret true
        else:
            print fn + " = NO ROAD" #DEBUG
            #ret false