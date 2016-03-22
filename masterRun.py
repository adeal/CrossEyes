import listOfDetectionFiles.py


#%--------------------READ IMAGE--------------------%

camera = picamera.PiCamera()
vibration_motor = 5
buzzer_motor = 6

while True:
    camera.capture('input.jpg')
    inputPhoto = cv2.imread('input.jpg')
    cv2.imshow('image', inputPhoto)
    cv2.waitKey(10)

    
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
    # print threeFourthsDown
    croppedInputPhoto = resizedInputPhoto[0:threeFourthsDown, :]
    # cv2.imshow('image', croppedInputPhoto)
    # cv2.waitKey(0)


    #%--------------CALL THE PROCESSES IN PARALLEL-----------------%

    detectStopSign(croppedInputPhoto)
    detectCrosswalkSign(croppedInputPhoto)
    detectRoad(croppedInputPhoto)




