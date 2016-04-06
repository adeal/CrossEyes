# import numpy as np
import cv2
import heapq
import os


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

# while True:
for fn in os.listdir('linesOnly'):
    print "\nProcessing new image..."
    inputPhoto = cv2.imread('linesOnly/' + fn)
    cv2.imshow('Input Photo', inputPhoto)
    cv2.moveWindow('Input Photo', 0, 0)
    cv2.waitKey(0)

    cv2.destroyWindow('Input Photo')

# inputPhoto = cv2.imread('roadFiles/20160316_142627.jpg')

    height, width, channels = inputPhoto.shape
    # print height, width

    if height > width:
        translationFactor = 400.0 / height
    else:
        translationFactor = 400.0 / width
    # print translationFactor

    # resize the image so the longest edge is 1200 pixels, keeping the same aspect ratio
    resizedInputPhoto = cv2.resize(inputPhoto, None, fx=translationFactor, fy=translationFactor, interpolation=cv2.INTER_CUBIC)
    height = resizedInputPhoto.shape[0]
    # print inputPhoto.shape[0]
    # print resizedInputPhoto.shape[0]
    # print threeFourthsDown
    # croppedInputPhoto = resizedInputPhoto[height / 4:height, :]
    cv2.imshow('Cropped Image', resizedInputPhoto)
    cv2.moveWindow('Cropped Image', 0, 0)
    cv2.waitKey(0)

    gray_img = cv2.cvtColor(resizedInputPhoto, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray', gray)
    # cv2.waitKey(0)
    ret, gray_img = cv2.threshold(gray_img, 165, 255, cv2.THRESH_BINARY)
    cv2.imshow('Thresholded Image', gray_img)
    cv2.moveWindow('Thresholded Image', 0, 0)
    cv2.waitKey(0)
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
                midPt = (x + x + w) / 2
                # cv2.line(croppedInputPhoto, (midPt, 0), (midPt, height), (0,255,0), 1)

                midptMedian.insert(midPt)
                possibleLines[i] = [x, y, w, h]

                # cv2.drawContours(croppedInputPhoto, contours, i, (0,255,0), 3)
                # cv2.imshow('contours', croppedInputPhoto)
                # cv2.waitKey(0)

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

    if len(crossLineContourIndexes) >= 3:
        print "CROSSWALK DETECTED"
        for contour in crossLineContourIndexes:
            cv2.drawContours(resizedInputPhoto, contours, contour, (0, 255, 0), 3)

    cv2.imshow('FINAL IMAGE', resizedInputPhoto)
    cv2.moveWindow('FINAL IMAGE', 0, 0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
