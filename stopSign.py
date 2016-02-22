import numpy as np
import cv2


#diego
#%--------------------READ IMAGE--------------------%
inputPhoto = cv2.imread('CVInput/stop.jpg')
cv2.imshow('image', inputPhoto)
cv2.waitKey(0)



#%--------------------RESIZE IMAGE--------------------%
#make longest edge 400

#get dimensions of image
height, width, channels = inputPhoto.shape
#print height, width

if height > width:
	translationFactor = 1200.0 / height
else:
	translationFactor = 1200.0 / width
#print translationFactor

#resize the image so the longest edge is 1200 pixels, keeping the same aspect ratio
resizedInputPhoto = cv2.resize(inputPhoto,None,fx=translationFactor, fy=translationFactor, interpolation = cv2.INTER_CUBIC)
#cv2.imshow('image', resizedInputPhoto)
#cv2.waitKey(0)

#crop the bottom 4th of the image
threeFourthsDown = resizedInputPhoto.shape[0] * (3.0 / 4)
print inputPhoto.shape[0]
print resizedInputPhoto.shape[0]
print threeFourthsDown

croppedInputPhoto = resizedInputPhoto[0:threeFourthsDown, :] # Crop from x, y, w, h -> 100, 200, 300, 400
# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
cv2.imshow('image', croppedInputPhoto)
cv2.waitKey(0)


#%--------------------THRESHOLD IMAGE--------------------%





#austin
#for this part, use the Thresholded_Images
#%--------------------DETECT BLOBS--------------------%