from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#Kill gphoto2 process that
#starts whenever we connect the
#camera

def killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout = subprocess.PIPE)
    out, err = p.communicate()

    #search for the line that has the process
    #we want to kill
    for line in out.splitlines():
        if b'' in line:
            #kill the process
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)

shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
picID = "PiShot"


clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", \
                "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_time
#save_loc = "/home/pi/Desktop/gphoto2/images/" + folder_name
save_loc = "/home/pi/Desktop/gphoto2/images/"

def create_save_folder():
    try:
        os.makedirs(save_loc)
    except:
        print("Failed to create the new directory")
    os.chdir(save_loc)


def captureImages():
    gp(triggerCommand)
    sleep(3)
    gp(downloadCommand)
    gp(clearCommand)

def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                os.rename(filename, (shot_time + ID + ".JPG"))
                print("Renamed the JPG")

GPIO.setup(16, GPIO.IN)

while True:
    if GPIO.input(16) == 1:
        gp(clearCommand)
        create_save_folder()
        captureImages()
        sleep(2)
        #captureImages()
        renameFiles(picID)
    #else:
    #    print("kein strom")
    #    sleep(5)
                   

