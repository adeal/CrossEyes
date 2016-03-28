import pygame
import pygame.camera
import sys
import os
from time import sleep
pygame.init()
pygame.camera.init()

screen = pygame.display.set_mode((640,480),0)

#os.system("sudo ./usbreset /dev/bus/usb/001/" + os.popen("lsusb | grep 'C270' | grep -o 'Device....' | grep -o '...$'").read())


cam_list = pygame.camera.list_cameras()

webcam = pygame.camera.Camera(cam_list[0],(32,24))
webcam.start()

while True:
	#os.system("sudo ./usbreset /dev/bus/usb/001/" + os.popen("lsusb | grep 'C270' | grep -o 'Device....' | grep -o '...$'").read())
	sleep(2)
	pygame.init()
	pygame.camera.init()
	screen = pygame.display.set_mode((640,480),0)
	cam_list = pygame.camera.list_cameras()
	webcam = pygame.camera.Camera(cam_list[0],(32,24))
	webcam.start()
	imagen = webcam.get_image()
	imagen = pygame.transform.scale(imagen, (640,480))
	scale.blit(imagen,(0,0))
	pygame.display.update()
	
