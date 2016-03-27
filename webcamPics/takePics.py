import os
from time import sleep 

i = 1;
while True:
    os.system("sudo ./usbreset /dev/bus/usb/001/" + os.popen("lsusb | grep 'C270' | grep -o 'Device....' | grep -o '...$'").read())
    os.system("fswebcam input" + str(i) + ".jpg -r 1280x720")
    sleep(5)
    i = i + 1
