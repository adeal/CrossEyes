from threading import Thread
import cv2
import numpy as np
import time
import grovepi
import heapq
import os
from time import sleep

#global variables
triggerFound = False
vibration_motor = 8
buzzer_motor = 7
imageEdge = 400.0

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
        try:
            if self.N % 2 == 0:
                return (-1 * self.maxHeap[0] + self.minHeap[0]) / 2.0
            else:
                return -1 * self.maxHeap[0]
        except:
            return -1



def detectCrosswalkLines(resizedInputPhoto):
    # print inputPhoto.shape[0]
    # print resizedInputPhoto.shape[0]
    # print threeFourthsDown
    # croppedInputPhoto = resizedInputPhoto[height / 4:height, :]

    #cv2.imshow('Cropped Image', resizedInputPhoto)
    #cv2.moveWindow('Cropped Image', 0, 0)
    #cv2.waitKey(30)

    gray_img = cv2.cvtColor(resizedInputPhoto, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray', gray)
    # cv2.waitKey(0)
    ret, gray_img = cv2.threshold(gray_img, 165, 255, cv2.THRESH_BINARY)
    #cv2.imshow('Thresholded Image', gray_img)
    #cv2.moveWindow('Thresholded Image', 0, 0)
    #cv2.waitKey(30)
    # gray2 = gray.copy()
    # mask = np.zeros(gray.shape,np.uint8)

    img, contours, _ = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('img', img)
    # cv2.waitKey(3000)

    numContours = len(contours)
    possibleLines = {}
    midptMedian = streamMedian()
    if numContours > 0:
        for i in range(0, numContours):
            area = cv2.contourArea(contours[i], False)
            # print "area of this contour is " + str(area)
            # make sure the contour is large enough to even bother with
            if area > 100:
                x, y, w, h = cv2.boundingRect(contours[i])
                if w > 3*h:
                    midPt = (x + x + w) / 2
                    # cv2.line(croppedInputPhoto, (midPt, 0), (midPt, height), (0,255,0), 1)

                    midptMedian.insert(midPt)
                    possibleLines[i] = [x, y, w, h]

                    # cv2.drawContours(croppedInputPhoto, contours, i, (0,255,0), 3)
                    # cv2.imshow('contours', croppedInputPhoto)
                    # cv2.waitKey(0)

    crossLineContourIndexes = []
    try: 
        median = midptMedian.getMedian()
    except:
        return
    # print "ok, done. median is: ", median
    for key, val in possibleLines.iteritems():
        x = val[0]
        w = val[2]

        midPt = (x + x + w) / 2
        # print "MIDPT for {} is {}".format(key, midPt)
        if ((median - (imageEdge) / 10) <= midPt <= (median + (imageEdge / 10))):
            crossLineContourIndexes.append(key)

    if len(crossLineContourIndexes) >= 3:
        print "CROSSWALK DETECTED"
        for contour in crossLineContourIndexes:
            cv2.drawContours(resizedInputPhoto, contours, contour, (0, 255, 0), 3)
            global triggerFound
            triggerFound = True

    #cv2.imshow('FINAL IMAGE', resizedInputPhoto)
    #cv2.moveWindow('FINAL IMAGE', 0, 0)
    #cv2.waitKey(30)
    #cv2.destroyAllWindows()

def sendAlertSignal():
    global triggerFound
    triggerFound = False
    grovepi.digitalWrite(vibration_motor,1)
    #spend 3 seconds making 3 beeps
    for i in range(1,3):
        grovepi.digitalWrite(buzzer_motor,1)
        time.sleep(0.3)
        grovepi.digitalWrite(buzzer_motor,0)
        time.sleep(0.3)
    #end vibration
    grovepi.digitalWrite(vibration_motor,0)

#Code Start
alertThread = Thread(target = sendAlertSignal, args = ())
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
        
        # call crosswalk lines only
        detectCrosswalkLines(resizedInputPhoto)
        #make sure ports aren't already in use
        #this code is replaced by the alertThread.join below
        #grovepi.digitalWrite(7,0)
        #grovepi.digitalWrite(8,0)
        
        if triggerFound:
            sendAlertSignal()
            if currentPic < 1000:
                cv2.imwrite("/home/pi/CrossEyes/crosseyesPicLog/positivePhoto_" + str(currentPic) + ".jpg", inputPhoto)
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
