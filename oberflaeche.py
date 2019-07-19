from tkinter import *
from threading import Thread
import RPi.GPIO as GPIO
import signal
import os
import subprocess
import time
from PIL import Image
from sh import gphoto2 as gp
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.IN)

sleep_time=0.2
gpio_pin=16

picID = "PiShot"

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", \
                "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

save_loc = "/home/pi/Desktop/gphoto2/images/"

class check_button(Thread):

    def __init__(self, labelText, x):
        Thread.__init__(self)
        self.labelText = labelText
        self.my_shot_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.x = x
        self.b = False

    def captureImages(self):
        self.my_shot_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
        gp(triggerCommand)
        time.sleep(3)
        gp(downloadCommand)
        gp(clearCommand)

    def renameFiles(self, ID):
        for filename in os.listdir("."):
            if len(filename) < 13:
                if filename.endswith(".JPG"):
                    os.rename(filename, (self.my_shot_time + ".JPG")) 

    def checkloop(self):
        while True:
            time.sleep(sleep_time)
            
            if GPIO.input(gpio_pin) == 1:
                my_countdown = 5
                
                while my_countdown > 0:
                    time.sleep(1)
                    self.labelText.set(my_countdown)
                    my_countdown -= 1

                self.labelText.set("Cheeeeese!")

                os.chdir(save_loc)
            
                gp(clearCommand)
                self.captureImages()
                self.labelText.set("Bitte warten!....")
                
                self.renameFiles(picID)
                im = Image.open(self.my_shot_time+'.JPG')
                im.save(self.my_shot_time+'.png')
                img = PhotoImage(file=self.my_shot_time+".png") #JPG files don't work!!!
                
                self.x.configure(image=img)
                self.x.image = img                

                self.b = True
                photofile = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Desktop/gphoto2/images/"+self.my_shot_time+".JPG "+self.my_shot_time+".jpg"
                subprocess.call([photofile], shell=True)
                    
                #time.sleep(5)
            else:
                self.x.configure(image='')
                
                self.labelText.set("Bitte auf Buzzer drücken")
                self.b = False
                

mamdouh = Tk()
mamdouh.attributes("-fullscreen", True)
labelText1 = StringVar()
x1 = Label(mamdouh,textvariable=labelText1) 
x1.config(font=('Helvetica',60,'bold'))
x1.grid(row=0,column=0)
x1.pack(padx=100, pady=100)
#mamdouh.title("mamdouh")
#mamdouh.geometry('1200x700')


chk1 = check_button(labelText1, x1)
c1 = Thread(target=chk1.checkloop)
c1.start()

mamdouh.mainloop()
