from threading import Thread
import copy
#import thread
#import picamera
import cv2
import numpy as np
import time
#import grovepi
import heapq
import os
from time import sleep

#global variables
translationFactorAmount = 400.0
# stopTriggerFound = False
# crossTriggerFound = False


def detectStopSign(resizedInputPhoto):
#%--------------------THRESHOLD IMAGE--------------------%
    # threeFourthsDown = resizedInputPhoto.shape[0] * (3.0 / 4)
    # croppedInputPhoto = resizedInputPhoto[0:threeFourthsDown, :]
    for i in range(0, resizedInputPhoto.shape[0]):
        for j in range(0, resizedInputPhoto.shape[1]):
            colorOfPixel = resizedInputPhoto[i, j]
            blue = colorOfPixel[0] + 0.0;
            green = colorOfPixel[1] + 0.0;
            red = colorOfPixel[2] + 0.0;

            if blue == 0.0:
                blue = 1
            if green == 0.0:
                green = 1
            if red / (blue + green) > 1.0 and abs(blue - green) < 50:
                resizedInputPhoto[i, j] = [255, 255, 255]
            else: #else, make it black
                resizedInputPhoto[i, j] = [0, 0, 0]

    #%--------------------DETECT BLOBS--------------------%
    gray_img = cv2.cvtColor(resizedInputPhoto, cv2.COLOR_BGR2GRAY)

    img, contours, _ = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('thresholded stop image', resizedInputPhoto)
    cv2.waitKey(30)
    if len(contours) > 0:
        numberOfContours = len(contours)
        largestArea = 0
        bestContour = -1
        allContours = copy.copy(resizedInputPhoto)
        for i in range(0, numberOfContours):
            #cv2.drawContours(allContours, contours, i, (0,255,0), 2)
            area = cv2.contourArea(contours[i], False)
            if area > 700/(translationFactorAmount/400): #original error measured w.r.t. 400
                #print "found stop contour bigger than 700"
                x,y,w,h = cv2.boundingRect(contours[i])
                #print float(w) / float(h)
                #print float(h) / float(w)
                if float(w) / float(h) > 0.8 and float(w) / float(h) < 1.2 and float(h) / float(w) > 0.8 and float(h) / float(w) < 1.2:
                    if area > largestArea:
                        largestArea = area
                        bestContour = i

        
        if bestContour >= 0:
            #print "STOP SIGN DETECTED"
            cv2.drawContours(resizedInputPhoto, contours, bestContour, (0,255,0), 2)
            cv2.imshow('final stop contour', resizedInputPhoto)
            cv2.waitKey(30)
            return True
        else:
            #print "NO STOP SIGN FOUND"
            noPhoto = cv2.imread('noStop.jpg')
            cv2.imshow('final stop contour', noPhoto)
            cv2.waitKey(30)
            return False
            #cv2.drawContours(croppedInputPhoto, contours, bestContour, (0,255,0), 2) #DEBUG
            #cv2.imshow('contours', croppedInputPhoto) #DEBUG
            #cv2.waitKey(3000) #DEBUG
        #print "STOP SIGN DONE"
    noPhoto = cv2.imread('noStop.jpg')
    cv2.imshow('final stop contour', noPhoto)
    cv2.waitKey(30)
    return False



def detectCrosswalkSign(resizedInputPhoto):
    #cv2.imshow('image', resizedInputPhoto)
    #cv2.waitKey(3000)
    # threeFourthsDown = resizedInputPhoto.shape[0] * (3.0 / 4)
    # croppedInputPhoto = resizedInputPhoto[0:threeFourthsDown, :]
    #cv2.imshow('image', croppedInputPhoto)
    #cv2.waitKey(3000)
    for i in range(0, resizedInputPhoto.shape[0]):
        for j in range(0, resizedInputPhoto.shape[1]):
            colorOfPixel = resizedInputPhoto[i, j]
            blue = colorOfPixel[0] + 0.0;
            green = colorOfPixel[1] + 0.0;
            red = colorOfPixel[2] + 0.0;

            if blue == 0.0:
                blue = 1
            if green == 0.0:
                green = 1
            if red == 0.0:
                red = 1         
            if red / blue > 1.6 and green / blue > 1.3 and red / green > 0.9:
                resizedInputPhoto[i, j] = [255, 255, 255]
            else: #else, make it black
                resizedInputPhoto[i, j] = [0, 0, 0]

    #%--------------------DETECT BLOBS--------------------%
    #print "about to detect blobs"
    gray_img = cv2.cvtColor(resizedInputPhoto, cv2.COLOR_BGR2GRAY)
    img, contours, _ = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('thresholded cross image', resizedInputPhoto) 
    cv2.waitKey(30)
    if len(contours) > 0:
        #print "found " + str(len(contours))+" contours"
        numberOfContours = len(contours)
        area = cv2.contourArea(contours[0], False)
        largestArea = 0
        bestContour = -1
        for i in range(0, numberOfContours):
            area = cv2.contourArea(contours[i], False)
            if area > 2000/(translationFactorAmount/400): #original area measured w.r.t. 400
                #print "found cross contour bigger than 2000"
                x,y,w,h = cv2.boundingRect(contours[i])
                if float(w) / float(h) > 0.4 and float(w) / float(h) < 1.6 and float(h) / float(w) > 0.4 and float(h) / float(w) < 1.6:
                    if area > largestArea:
                        largestArea = area
                        bestContour = i
        
               
        if bestContour >= 0:
            #print "CROSSWALK SIGN DETECTED"
            cv2.drawContours(resizedInputPhoto, contours, bestContour, (0,255,0), 2)
            cv2.imshow('final cross contour', resizedInputPhoto)
            cv2.waitKey(30)

            return True
        else:
            noPhoto = cv2.imread('noCross.jpg')
            cv2.imshow('final cross contour', noPhoto)
            cv2.waitKey(30)
            #print "NO CROSSWALK SIGN FOUND"
            return False
        #end vibration
        #grovepi.digitalWrite(vibration_motor,0)
        #grovepi.digitalWrite(7,0)
        #cv2.drawContours(croppedInputPhoto, contours, bestContour, (0,255,0), 2) #DEBUG
        #cv2.imshow('contours', croppedInputPhoto) #DEBUG
        #cv2.waitKey(3000) #DEBUG
    noPhoto = cv2.imread('noCross.jpg')
    cv2.imshow('final cross contour', noPhoto)
    cv2.waitKey(30)
    return False





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

            #%-------------------DETECT FEATURES------------------%
            crossPhoto = copy.copy(resizedInputPhoto)
            stopTriggerFound = detectStopSign(resizedInputPhoto)
            crossTriggerFound = detectCrosswalkSign(crossPhoto)

            

            if stopTriggerFound and not crossTriggerFound:
                print "found stop sign but not crosswalk sign"
            elif not stopTriggerFound and crossTriggerFound:
                print "found crosswalk sign but no stop sign"
            elif stopTriggerFound and crossTriggerFound:
                print "found both stop sign and crosswalk sign"
            else:
                print "NOTHING FOUND"


            cv2.waitKey(0)
          

            
       

    
