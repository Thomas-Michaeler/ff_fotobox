from tkinter import *
from threading import Thread
import RPi.GPIO as GPIO
import signal
import os
import subprocess
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#from sh import gphoto2 as gp
from datetime import datetime
from picamera import PiCamera

GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.IN)

sleep_time=0.2
gpio_pin=16

picID = "PiShot"

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", \
                "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

#save location using gphoto2
save_loc = "/home/pi/Desktop/images/"

#sav location using pi camera
save_loc_pi = "/home/pi/Desktop/images/"


camera = PiCamera()

class check_button(Thread):

    def __init__(self, labelText, x):
        Thread.__init__(self)
        self.labelText = labelText
        self.my_shot_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.x = x
        self.b = False

    def captureImages(self):
        self.my_shot_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
        #gp(triggerCommand)
        time.sleep(3)
        #gp(downloadCommand)
        #gp(clearCommand)
        
    def captureImagesPiCamera(self):
        self.my_shot_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        camera.start_preview()
        time.sleep(5)
        camera.capture(save_loc_pi + '' + self.my_shot_time + ".JPG")
        camera.stop_preview()
        
    def renameFiles(self, ID):
        for filename in os.listdir("."):
            if len(filename) < 13:
                if filename.endswith(".JPG"):
                    os.rename(filename, (self.my_shot_time + ".JPG")) 

    def checkloop(self):
        while True:
            time.sleep(sleep_time)
            
            if GPIO.input(gpio_pin) == 0:
                my_countdown = 6

                os.chdir(save_loc)
                
                while my_countdown > 1:
                    my_countdown -= 1
                    self.labelText.set(my_countdown)
                    time.sleep(1)
                    

                self.labelText.set("Cheeeeese!")
                
                #when using gphoto2
                #gp(clearCommand)
                self.captureImagesPiCamera()
                self.labelText.set("Bitte warten!....")
                
                #when using gphoto2
                #self.renameFiles(picID)
                im = Image.open(self.my_shot_time+'.JPG')
                im2 = Image.open(self.my_shot_time+'.JPG')
                
                size = 1080, 1080
                im.thumbnail(size)
                im.save(self.my_shot_time+'.png')


                #Watermark setzen!!!
                watermark = Image.new("RGBA", im2.size)

                waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")
                my_font = ImageFont.truetype("FreeSans.ttf",50)
                #waterdraw.text((100,100), "@Steinbruchfest 2018", font=my_font, fill="green")
                waterdraw.text((0,0), "@Steinbruchfest 2018", font=my_font)

                #min(x, y), y = 0 nichts, y = 200 voll drauf (und weiss)
                watermask = watermark.convert("L").point(lambda x: min(x, 255))

                watermark.putalpha(watermask)

                im2.paste(watermark, None, watermark)
                im2.save('watermarked_'+self.my_shot_time+'.jpg')

                #watermark setzen vorbei!!! 
                
                img = PhotoImage(file=self.my_shot_time+".png") #JPG files don't work!!!
                
                self.x.configure(image=img)
                self.x.image = img

                self.b = True

                #Dropbox-Upload
                #photofile = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Desktop/gphoto2/images/watermarked_"+self.my_shot_time+".jpg /Steinbruchfest_2018/Steinbruchfest_2018_"+self.my_shot_time+".jpg"
                #subprocess.call([photofile], shell=True)
                    
                time.sleep(5)
            else:
                self.x.configure(image='')
                
                self.labelText.set("Bitte auf Buzzer druecken")
                self.b = False
                

mamdouh = Tk()
mamdouh.attributes("-fullscreen", True)
labelText1 = StringVar()
x1 = Label(mamdouh,textvariable=labelText1) 
x1.config(font=('Helvetica',65,'bold'))
#x1.grid(row=0,column=0)
x1.pack(padx=100, pady=100)

#mamdouh.title("mamdouh")
#mamdouh.geometry('1200x700')


chk1 = check_button(labelText1, x1)
c1 = Thread(target=chk1.checkloop)
c1.start()

mamdouh.mainloop()
