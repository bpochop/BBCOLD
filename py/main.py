import tkinter as tk
import json as json
from tkinter import ttk, messagebox
import pyfirmata
import asyncio
import time as t
import threading
# import RPi.GPIO as GPIO
# from rpi_ws281x import *
import argparse


width = 125
height = 80

"""
shot: 1.5

small:3
medium: 5
large: 7

Small: 90
Medium: 150
Large: 210


TODO:

set python interpeter!

    imprtant:
        LED's get middle to light up
        do LED code
        
        

    extra:  
        getscroll wheel to work
        create function
        make a drink stronger
        clean up code;
            add extra files
            add helperMasterClass (read and writing and shit)
            

"""


small_mili = 90
medium_mili = 150
large_mili = 210
shot_mili = 40



nread = open("../data/pumps.json", "r")
d = json.load(nread)
pumps = []
for x in d:
    pumps.append(d[x])
nread.close()

nread = open("../data/recipes.json", "r")
d = json.load(nread)
recipes = d["drinks"]
shotrecipies = d["shot"]
nread.close()

read = open("../data/display.json", "r")
linedata = json.load(read)
read.close()


read = open("../data/theme.json", "r")
theme = json.load(read)
read.close()

# LED strip configuration:
LED_COUNT      = 93      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 5     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


'''
#intializing arduino board/usb to a variable

#board0 = arduino inside main station
board0 = pyfirmata.Arduino('/dev/ttyUSB0')
#board1 = pump station 1
board1 = pyfirmata.Arduino('/dev/ttyUSB1')
#board2 = pump station 2
board2 = pyfirmata.Arduino('/dev/ttyUSB2')






####Intializing arduino pin to a variable. ex. pump1_3 = pump station #1 pump#3

#pump station 1
pump1_1 = board1.get_pin('d:2:o')
pump1_2 = board1.get_pin('d:3:o')
pump1_3 = board1.get_pin('d:4:o')
pump1_4 = board1.get_pin('d:5:o')
pump1_5 = board1.get_pin('d:6:o')
pump1_6 = board1.get_pin('d:7:o')
pump1_7 = board1.get_pin('d:8:o')
pump1_8 = board1.get_pin('d:9:o')

#pump station 2
pump2_1 = board2.get_pin('d:2:o')
pump2_2 = board2.get_pin('d:3:o')
pump2_3 = board2.get_pin('d:4:o')
pump2_4 = board2.get_pin('d:5:o')
pump2_5 = board2.get_pin('d:6:o')
pump2_6 = board2.get_pin('d:7:o')
pump2_7 = board2.get_pin('d:8:o')
pump2_8 = board2.get_pin('d:9:o')

####Initializing arduino pin for the steppper motor inside main station
stepper_motor_dir = board0.get_pin('d:2:o')
stepper_motor_step = board0.get_pin('d:3:o')
stepper_motor_enable = board0.get_pin('d:7:o')
mixer_motor = board0.get_pin('d:4:o')

#makes sure pumps are off (1 = "OFF" specifically for the pumps)
pump1_1.write(1)
pump1_2.write(1)
pump1_3.write(1)
pump1_4.write(1)
pump1_5.write(1)
pump1_6.write(1)
pump1_7.write(1)
pump1_8.write(1)
pump2_1.write(1)
pump2_2.write(1)
pump2_3.write(1)
pump2_4.write(1)
pump2_5.write(1)
pump2_6.write(1)
pump2_7.write(1)
pump2_8.write(1)

#makes sure mixer motor is off
mixer_motor.write(1)
stepper_motor_enable.write(0)

#Values to control stepper motor
step_count = 1950 #length of up and down
delay = .0005     #speed of up and down


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()


class LED():
    def __init__(self):
        self.LEDdone = True

    def mainLoop(self, strip):
        pass
        done = True
        while done:
            self.colorWipe(strip, Color(0, 0, 0), 10)  # This will slowsly turn off all LED...
            # i.e. the crosshair, before it starts animation
            self.colorWipe(strip, Color(127, 0, 0))  # Red wipe
            self.checkIfDone()
            self.colorWipe(strip, Color(127, 127, 127))  # White wipe
            self.checkIfDone()
            self.colorWipe(strip, Color(000, 000, 127))  # Blue wipe
            self.checkIfDone()
            self.theaterChase(strip, Color(0, 0, 127))  # Blue theater chase
            self.checkIfDone()
            self.theaterChase(strip, Color(127, 127, 127))  # White theater chase
            self.checkIfDone()
            self.theaterChase(strip, Color(127, 0, 0))  # Red theater chase
            self.checkIfDone()
            self.rainbow(strip)
            self.checkIfDone()
            self.rainbowCycle(strip)
            self.checkIfDone()
            self.theaterChaseRainbow(strip)
            self.checkIfDone()
            done = False
#             if LEDdone = False:
#                 break

    def checkIfDone(self):
        return done, self.LEDdone
    
    def LEDISDONE(self):
        done = False
        self.LEDdone = False
        return done, self.LEDdone


    def colorCupPlacement(self, strip):
        for i in range(72, 84):
            strip.setPixelColor(i, Color(255, 0, 0))
            strip.show()
        for i in range(84, 93):
            strip.setPixelColor(i, Color(255, 255, 255))
            strip.show()

        strip.setPixelColor(24, Color(255, 0, 0))
        strip.setPixelColor(50, Color(255, 0, 0))
        strip.setPixelColor(68, Color(255, 0, 0))
        strip.setPixelColor(8, Color(255, 0, 0))
        strip.setPixelColor(38, Color(255, 0, 0))
        strip.setPixelColor(60, Color(255, 0, 0))
        strip.setPixelColor(0, Color(255, 0, 0))
        strip.setPixelColor(32, Color(255, 0, 0))
        strip.setPixelColor(56, Color(255, 0, 0))
        strip.setPixelColor(16, Color(255, 0, 0))
        strip.setPixelColor(44, Color(255, 0, 0))
        strip.setPixelColor(64, Color(255, 0, 0))
        strip.show()


    def colorWipe(self, strip, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(int(LED_COUNT)):
            strip.setPixelColor(i, color)
            strip.show()
            t.sleep(wait_ms / 2000.0)


    def theaterChase(self, strip, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, int(LED_COUNT), 3):
                    strip.setPixelColor(i + q, color)
                strip.show()
                t.sleep(wait_ms / 1000.0)
                for i in range(0, int(LED_COUNT), 3):
                    strip.setPixelColor(i + q, 0)


    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)


    def rainbow(self, strip, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(int(LED_COUNT)):
                strip.setPixelColor(i, self.wheel((i + j) & 255))
            strip.show()
            t.sleep(wait_ms / 1000.0)


    def rainbowCycle(self, strip, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * iterations):
            for i in range(int(LED_COUNT)):
                strip.setPixelColor(i, self.wheel((int(i * 256 / int(LED_COUNT)) + j) & 255))
            strip.show()
            t.sleep(wait_ms / 1000.0)


    def theaterChaseRainbow(self, strip, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, int(LED_COUNT), 3):
                    strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                strip.show()
                t.sleep(wait_ms / 2000.0)
                for i in range(0, int(LED_COUNT), 3):
                    strip.setPixelColor(i + q, 0)

    def checkIfDone(self):
        return 


led = LED()
'''

class dispenseLayout():
    def __init__(self, master, content, obj, ratio, dtype):
        self.master = master

        master.title = "Confirm"

        self.done_dispensing = True
        self.frame = tk.Frame(self.master)
        self.frame2 = tk.Frame(self.master)

        self.frame.grid(row = 0,padx =60, pady =10, sticky = "nsew")
        self.frame2.grid(row=1, padx = 60, pady =10, sticky = "nsew")


        if dtype =="cock":
            self.setLayout(content,obj, ratio)
        else:
            self.shotsetLayout(content,obj,ratio)

        self.ingrediants = []

        for x in content:
            self.ingrediants.append(content[x])


    def shotsetLayout(self, content, obj, ratio):

        description = ""
        for y in range(len(content)):
            name = "l" + str(y + 1)
            rname = "l" + str(y + 1) + "r"
            description += "\n" + str(int(ratio[rname] * 100)) + "%   " + content[name]

        self.pictureLabel = tk.Label(
            self.frame,
            image=obj["img"]
        )

        self.drinkLabel = tk.Label(
            self.frame,
            text=obj["name"] + "\n" + description,
            compound="left"
        )


        if self.done_dispensing:
            self.mediumButton = tk.Button(
                self.frame2,
                text="CONFIRM",
                command=lambda: self.createloadingwindow(content, ratio, shot_mili),
                padx=90,
                pady=30,
                bg=theme["size_button_color"]
            )
        else:
            self.mediumButton = tk.Label(
                self.frame2,
                text="NOT DONE DISPENSING PREVIOUS DRINK",
                padx=50,
                pady=30,
                bg=theme["size_button_color"]
            )

        self.pictureLabel.grid(row=0, column=0, padx=10, pady=60, sticky="nsew")
        self.drinkLabel.grid(row=0, column=1, padx=60, pady=60, sticky="nsew")
        self.mediumButton.grid(row=1, column=1, padx=120, pady=60, sticky="nsew")


    def setLayout(self,content,obj,ratio):

        description = ""
        for y in range(len(content)):
            name = "l" + str(y + 1)
            rname = "l" + str(y + 1) + "r"
            if not isinstance(ratio[rname],str):
                description += "\n" + str(int(ratio[rname] *100)) + "%   " + content[name].title()
            else:
                description += "\n" + content[name].title()


        self.pictureLabel = tk.Label(
            self.frame,
            image = obj["img"]
        )
        self.pictureLabel.grid(row = 0, column =0, padx =10, pady =60, sticky = "nsew")



        self.drinkLabel = tk.Label(
            self.frame,
            text = obj["name"] + "\n" +description,
            compound = "left"
        )
        self.drinkLabel.grid(row = 0, column =1, padx =60, pady =60, sticky = "nsew")

        if self.done_dispensing:
            self.smallButton = tk.Button(
                self.frame2,
                text ="SMALL",
                command = lambda :self.createloadingwindow(content,ratio,small_mili),
                padx = 50,
                pady =30,
                bg = theme["size_button_color"]
            )
            self.mediumButton = tk.Button(
                self.frame2,
                text="MEDIUM",
                command=lambda :self.createloadingwindow(content, ratio, medium_mili),
                padx=90,
                pady=30,
                bg=theme["size_button_color"]
            )
            self.largeButton = tk.Button(
                self.frame2,
                text="LARGE",
                command=lambda :self.createloadingwindow(content, ratio, large_mili),
                padx=50,
                pady=30,
                bg=theme["size_button_color"]
            )
            self.smallButton.grid(row=1, column=0, padx=10, pady=60, sticky="nsew")
            self.mediumButton.grid(row=1, column=1, padx=10, pady=60, sticky="nsew")
            self.largeButton.grid(row=1, column=2, padx=10, pady=60, sticky="nsew")
        else:
            self.label = tk.Label(
                self.frame2,
                text = "NOT DONE DISPENSING PREVIOUS DRINK",
                padx = 50,
                pady =30,
                bg = theme["size_button_color"]
            )

    def createloadingwindow(self, content, ratio, dtype):
        self.done_dispensing = False
        self.async_loop = asyncio.get_event_loop()
        # t.sleep(5)
        s = t.perf_counter()

        thread1 = threading.Thread(target=self.buffer_function, args=(content, ratio, dtype))
        # thread2 = threading.Thread(target= self.setLED)

        thread1.start()
        # thread2.start()

        # led.LEDISDONE()
        # led.colorWipe(strip, Color(0, 0, 0))

        thread1.join()
        # thread2.join()
        self.master.destroy()

    def setLED(self):
        pass
        # led.mainLoop(strip)

    async def findPump(self,pumpdata, i, content, ratio, size):


        time = (ratio[i + "r"] * size) / 3
        z = ""
        for x in pumpdata:
            if content[i].title() in pumpdata[x]:

                z = x
                '''
                if z == "pump1_1":

                    pump1_1.write(0)
                    await asyncio.sleep(time)
                    pump1_1.write(1)
                    break

                if z == "pump1_2":

                    pump1_2.write(0)
                    await asyncio.sleep(time)
                    pump1_2.write(1)
                    break

                if z == "pump1_3":

                    pump1_3.write(0)
                    await asyncio.sleep(time)
                    pump1_3.write(1)
                    break

                if z == "pump1_4":

                    pump1_4.write(0)
                    await asyncio.sleep(time)
                    pump1_4.write(1)
                    break

                if z == "pump1_5":
                    pump1_5.write(0)
                    await asyncio.sleep(time)
                    pump1_5.write(1)
                    break

                if z == "pump1_6":
                    pump1_6.write(0)
                    await asyncio.sleep(time)
                    pump1_6.write(1)
                    break

                if z == "pump1_7":
                    pump1_7.write(0)
                    await asyncio.sleep(time)
                    pump1_7.write(1)
                    break

                if z == "pump1_8":
                    pump1_8.write(0)
                    await asyncio.sleep(time)
                    pump1_8.write(1)
                    break
                if z == "pump2_1":
                    pump2_1.write(0)
                    await asyncio.sleep(time)
                    pump2_1.write(1)
                    break

                if z == "pump2_2":
                    pump2_2.write(0)
                    await asyncio.sleep(time)
                    pump2_2.write(1)
                    break

                if z == "pump2_3":
                    pump2_3.write(0)
                    await asyncio.sleep(time)
                    pump2_3.write(1)
                    break

                if z == "pump2_4":
                    pump2_4.write(0)
                    await asyncio.sleep(time)
                    pump2_4.write(1)
                    break

                if z == "pump2_5":
                    pump2_5.write(0)
                    await asyncio.sleep(time)
                    pump2_5.write(1)
                    break

                if z == "pump2_6":
                    pump2_6.write(0)
                    await asyncio.sleep(time)
                    pump2_6.write(1)
                    break

                if z == "pump2_7":
                    pump2_7.write(0)
                    await asyncio.sleep(time)
                    pump2_7.write(1)
                    break

                if z == "pump2_8":
                    pump2_8.write(0)
                    await asyncio.sleep(time)
                    pump2_8.write(1)
                    break
'''



    async def mainLoop(self,content, ratio,size):

        read = open("../data/pumps.json", "r")
        pumpdata = json.load(read)
        read.close()

        pump = []

        for a in content:
            pump.append(self.async_loop.create_task(self.findPump(pumpdata, a, content, ratio, size)))

        await asyncio.wait(pump)

    def buffer_function(self,content,ratio,size):
        # self.setlayout()
        self.async_loop.run_until_complete(self.mainLoop(content,ratio, size))
        print("test")
        # stepper_motor_enable.write(0)
        # t.sleep(1)
        # self.down()
        # t.sleep(1)
        # self.spinMotor()
        # t.sleep(1)
        # self.up()

        self.done_dispensing = False
     
   
    def up(self):
        pass
    #     stepper_motor_dir.write(1)
    #     for x in range(step_count):
    # #         GPIO.output(STEP, GPIO.HIGH)
    #         stepper_motor_step.write(1)
    #         t.sleep(delay)
    #         stepper_motor_step.write(0)
    #         t.sleep(delay)
    #     stepper_motor_enable.write(1)

    def down(self):
        pass
        # stepper_motor_dir.write(0)
        #
        # for x in range(step_count):
        #     stepper_motor_step.write(1)
        #     t.sleep(delay)
        #     stepper_motor_step.write(0)
        #     t.sleep(delay)


    def spinMotor(self):
        pass
            #CHECK HERE FOR BUGS, ON 3RD DRINK IT KEPT SPINNING FOREVER!
            # mixer_motor.write(0)# turns on motor
            # t.sleep(5) #BUG HERE MAYBE? DIDNT WAKE UP
            # mixer_motor.write(1)

class menuLayout():
    def __init__(self, master):

        self.master = master

        try:
            self.style = ttk.Style()

            color1 = theme["tab_color1"]
            color2 = theme["tab_color2"]

            #TO CHANGE TAB WIDTH MESS WITH THE CONSTANT DIVIDING THE ENTIRE VALUE!
            self.swidth = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) /5

            self.style.theme_create("yummy", parent="alt", settings={
                "TNotebook": {"configure": {"tabmargins": [0, 0, 10, 0], "background": theme["tab_background_color"]}, "orient": "vertical"},
                "TNotebook.Tab": {
                    "configure": {"padding": [self.swidth, 25], "background": color1},
                    "map": {"background": [("selected", color2)],
                            "expand": [("selected", [1, 1, 1, 0])]}}})

            self.style.theme_use("yummy")
        except:
            self.style.theme_use("yummy")

        master.title = "DRINK MENU"

        self.canvas = tk.Canvas(self.master, width = 10)#self.master.winfo_reqwidth())

        print(self.canvas.winfo_screenheight())
        print(self.canvas.winfo_screenwidth())
        self.canvas.pack(side="left", fill="both", expand=1)

        self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side = "right", fill ="y",expand=0)

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.canvasheight = 9000

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(self.canvas, height=self.canvasheight, bg="black")
        self.interior_id = self.canvas.create_window(0, 0, window=interior, anchor="nw")

        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)


        self.canvas.configure(yscrollcommand =self.scrollbar.set,bg = theme["background_color"], highlightthickness = 0)
        try:
            self.canvas.bind('<Configure>', lambda e:self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            self.canvas.bind_all('<MouseWheel>', lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        except:
            pass


        self.offset_y = 0

        self.offset_y = 0
        self.prevy = 0
        self.scrollposition = 1



        self.canvas.bind("<Enter>", lambda _: self.canvas.bind_all('<Button-1>', self.on_press), '+')
        self.canvas.bind("<Leave>", lambda _: self.canvas.unbind_all('<Button-1>'), '+')
        self.canvas.bind("<Enter>", lambda _: self.canvas.bind_all('<B1-Motion>', self.on_touch_scroll), '+')
        self.canvas.bind("<Leave>", lambda _: self.canvas.unbind_all('<B1-Motion>'), '+')

        self.tablayout = ttk.Notebook(self.canvas)

        self.drinkTab = tk.Frame(self.tablayout, bg = theme["tab_background_color"])
        self.shotTab = tk.Frame(self.tablayout, bg = theme["tab_background_color"])
        self.backTab = tk.Frame(self.tablayout)

        self.backTab.bind("<Visibility>",lambda e: self.killitall())
        self.tablayout.add(self.drinkTab, text = "Drinks")
        self.tablayout.add(self.shotTab, text = "Shots")
        self.tablayout.add(self.backTab, text="Back")

        self.canvas.create_window((0,0), window=self.tablayout, anchor="nw")

        self.getLayout()


    def killitall(self):
        self.canvas.bind("<Leave>", lambda _: self.canvas.unbind_all('<Button-1>'),'+')
        self.canvas.bind("<Leave>",lambda _: self.canvas.unbind_all('<B1-Motion>'),'+')
        self.master.destroy()



        # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar
    def _configure_interior(self,event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.interior.winfo_reqwidth())


    def _configure_canvas(self,event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())


    def on_press(self,event):
        try:
            self.offset_y = event.y_root
            if self.scrollposition < 1:
                self.scrollposition = 1
            elif self.scrollposition > self.canvasheight:
                self.scrollposition = self.canvasheight
            self.canvas.yview_moveto(self.scrollposition / self.canvasheight)
        except:
            pass

    def on_touch_scroll(self,event):
        try:
            nowy = event.y_root

            sectionmoved = 40
            if nowy > self.prevy:
                event.delta = -sectionmoved
            elif nowy < self.prevy:
                event.delta = sectionmoved
            else:
                event.delta = 0
            self.prevy = nowy

            self.scrollposition += event.delta
            self.canvas.yview_moveto(self.scrollposition / self.canvasheight)
        except:
            pass

    def getLayout(self):

        row = 0
        column = 0
        read = open("../data/display.json", "r")
        linedata = json.load(read)
        read.close()

        read = open("../data/pumps.json", "r")
        pumpdata = json.load(read)
        read.close()

        p  = []

        for x in pumpdata:
            p.append(pumpdata[x])

        for x in range(0,len(recipes),linedata["display"]):

            for y in range(linedata["display"]):
                flag = True

                if column == linedata["display"]:
                    column = 0


                if y+x < len(recipes):

                    # check if each item of recipes[content] is in
                    # p(list of alcohol in pumps) is in
                    for z in recipes[y + x]["content"]:

                        if not recipes[y + x]["content"][z].title() in p:

                            if isinstance(recipes[y+x]["ratio"][z+"r"],str):
                                continue
                            flag = False
                            break

                    if flag is False:
                        continue




                    if not recipes[y + x]["img"] or recipes[y + x]["img"] == " ":
                        img = tk.PhotoImage(file="../img/default.png")
                    else:
                        # img = tk.PhotoImage(file="img/default.png")
                        img = tk.PhotoImage(file="../img/"+ str(recipes[y + x]["img"]))

                    content = recipes[y+x]["content"]
                    ratio = recipes[y+x]["ratio"]
                    values = {
                        "name":recipes[y+x]["name"],
                        "count":row,
                        "column": column,
                        "img": img
                    }
                    self.setButton(content,values,ratio, self.drinkTab,"cock")
                    column += 1

                if column == linedata["display"]:
                    row += 1



        column =0
        for x in range(0, len(shotrecipies), linedata["display"]):


            for y in range(linedata["display"]):

                flag = True

                if column == linedata["display"]:
                    column = 0

                if y + x < len(shotrecipies):
                    for z in shotrecipies[y + x]["content"]:

                        if not shotrecipies[y + x]["content"][z].title() in p:
                            if isinstance(shotrecipies[y + x]["ratio"][z + "r"], str):
                                continue
                            flag = False
                            break;

                    if flag is False:
                        continue

                    if not shotrecipies[y + x]["img"] or shotrecipies[y + x]["img"] == " ":
                        img = tk.PhotoImage(file="../img/default.png")
                    else:
                        # img = tk.PhotoImage(file="img/default.png")
                        img = tk.PhotoImage(file="../img/"+str(recipes[y + x]["img"]))

                    content = shotrecipies[y + x]["content"]
                    ratio = shotrecipies[y + x]["ratio"]
                    values = {
                        "name": shotrecipies[y + x]["name"],
                        "count": row,
                        "column": column,
                        "img": img
                    }
                    shot = "shot"
                    self.setButton(content, values, ratio, self.shotTab,shot)
                    column += 1

                if column == linedata["display"]:
                    row += 1


    def setButton(self,content, obj, ratio, tab, wildcard):

        read = open("../data/display.json", "r")
        linedata = json.load(read)
        read.close()

        # im2b = obj["img"]
        print(linedata["display"])
        if linedata["display"] == 1:
            x =0
            im2b = obj["img"]
        elif linedata["display"] >=3 and linedata["display"] <=5:
            x = linedata["display"] - 2
            im2b = obj["img"].subsample(x, x)
        elif linedata["display"] >=6:
            x = linedata["display"] +1
            im2b = obj["img"].subsample(x, x)
        else:
            x = linedata["display"] - 1
            im2b = obj["img"].subsample(x, x)




        description = obj['name'] + "\n"


        for y in range(len(content)):
            name = "l" + str(y + 1)
            description += "\n"+ content[name].title()

        self.button1 = tk.Button(
            tab,
            text=description,
            relief="flat",
            image = im2b,
            compound="left",
            highlightcolor=theme["button_highlight_color"],
            bg=theme["button_colors"],
            padx = 20,
            command = lambda :self.createDispenseMenu(content, obj,ratio, wildcard),
            )
        self.button1.image = im2b
        self.button1.grid(row=obj["count"], column=obj["column"], padx=5, pady=(20,5), sticky="nsew")

    def createDispenseMenu(self,content,obj,ratio,wildcard):

        self.dispenseMenu = tk.Toplevel(self.tablayout)
        self.dispenseMenu.attributes('-topmost', 'true')
        self.dispenseMenu.configure(bg='#f0f0f0')
        ##40E0D0

        file = open("../data/display.json", "r")
        data = json.load(file)
        file.close()

        posH = data["h"]
        posw = data["w"]

        self.dispenseMenu.geometry("+%d+%d"%(posH, posw))
        dispenseLayout(self.dispenseMenu,content,obj,ratio, wildcard)





class alcLayout():
    def __init__(self, master):
        self.master = master
        nread = open("../data/pumps.json", "r")
        d = json.load(nread)
        self.pumps = []
        for x in d:
            self.pumps.append(d[x])

        self.frame = tk.Frame(master)
        master.title = "Set Layout"
        self.getLayout()

        # Readin JSON data and check if there are any saved loadout configurations


    def getLayout(self):

        read = open("../data/drinks.json", "r")
        drinkdata = json.load(read)
        read.close()



        self.drinkList = []
        self.juicelist = []

        self.updatePumps = drinkdata["alcohol"]
        self.juicePumps = drinkdata["other"]

        for x in drinkdata["alcohol"]:
            self.drinkList.append(x)

        self.drinkList.sort()

        for x in drinkdata["other"]:
            self.juicelist.append(x)

        self.juicelist.sort()


        self.popmenu= {}
        self.juicemenu = {}
        self.displaymenu = {}
        self.display = [1,2,3,4,5,6,7,8,9,10]


        self.choices = {}
        self.juicechoices = {}
        self.displaychoices = {}

        #ADD JUICES BUTTON,


        aLabel = tk.Label(self.frame, text = "Alcohol").grid(row =0, column = 1)
        jLabel = tk.Label(self.frame, text = "Juice/Soda").grid(row = 0, column =2)

        for x in range(16):
            self.choices[x] = tk.StringVar(self.frame)
            self.juicechoices[x] = tk.StringVar(self.frame)

            if self.pumps[x] in self.drinkList:
                self.choices[x].set(self.pumps[x])
                self.juicechoices[x].set(" ")
            elif self.pumps[x] in self.juicelist:
                self.choices[x].set(" ")
                self.juicechoices[x].set(self.pumps[x])

            self.popmenu[x] = tk.OptionMenu(self.frame, self.choices[x], *self.drinkList)
            self.juicemenu[x] = tk.OptionMenu(self.frame, self.juicechoices[x], *self.juicelist)
            getAlc = tk.Label(self.frame,text="Pump " + str(x +1), justify = "left").grid(row = x+1, column = 0)

            self.popmenu[x].grid(row = x+1, column = 1)
            self.juicemenu[x].grid(row = x+1, column = 2)



        button = tk.Button(self.frame, text = "Save", command = self.saveList, padx = 40, pady=10).grid(row =17, column =0)
        button2 = tk.Button(self.frame, text = "Clear", command = self.clearList, padx = 40, pady =10). grid(row =17, column = 1)
        descriptionLabel = tk.Label(self.frame,text = "Drinks per Line",justify = "left")

        self.displaychoices = tk.StringVar(self.frame)
        self.displaychoices.set(linedata["display"])
        self.displaymenu = tk.OptionMenu(self.frame, self.displaychoices, *self.display)
        self.displaymenu.grid(row =18, column =1)
        descriptionLabel.grid(row=18, column =0)

        self.frame.pack()

    def clearList(self):
        for x in range(16):
            self.juicechoices[x].set(" ")
            self.choices[x].set(" ")



    def saveList(self):
        self.pumps = []

        self.lines = self.displaychoices.get()
        for x in self.choices:

            if self.choices[x].get() == " " and self.juicechoices[x].get() == " ":
                self.pumps.append(" ")
                continue

            if self.choices[x].get() == " ":
                self.pumps.append(self.juicechoices[x].get())
            else:
                self.pumps.append(self.choices[x].get())

        read = open("../data/pumps.json", "r")
        drinkdata = json.load(read)
        read.close()

        linedata["display"] = int(self.displaychoices.get())

        z = 0

        for x in drinkdata:
            if not self.pumps[z]:
                drinkdata[x] = " "
            else:
                drinkdata[x] = self.pumps[z]


            z+=1

        write = open("../data/pumps.json", "w")
        json.dump(drinkdata, write, indent=2)
        write.close()

        write = open("../data/display.json", "w")
        json.dump(linedata, write, indent=2)
        write.close()

        self.master.destroy()



class settingsLayout():
    def __init__(self, master):
        super(settingsLayout,self).__init__()

        self.master = master

        self.frame = tk.Frame(master)
        self.setLayout()
        self.frame.pack()

    def setLayout(self):
        # img4 = tk.PhotoImage(file="img/clean.png")
        self.cleanLabel = tk.Button(self.frame, text = "\tClean/Prime",
                                    command=self.clean,
                                    relief="flat",
                                    # image=img4,
                                   compound="left",
                                   highlightcolor=theme["button_highlight_color"],
                                   bg=theme["button_colors"])
        self.options = {}
        self.time = tk.StringVar(self.frame)
        self.time.set(" ")
        self.display = [1,2,3,4,5,6,7,8,9,10]

        self.timeMenu = tk.OptionMenu(self.frame, self.time, *self.display)



        self.MotorUpButton = tk.Button(self.frame,
                                       text = "\tMotor Up",
                                       command=self.motorUp,
                                       relief="flat",
                                       # image=img4,
                                       compound="left",
                                       highlightcolor=theme["button_highlight_color"],
                                       bg=theme["button_colors"]
                                       )

        self.motorDownButton = tk.Button(self.frame,
                                         text = "\tMotor Down",
                                         command = self.motorDown,
                                         relief="flat",
                                         # image=img4,
                                         compound="left",
                                         highlightcolor=theme["button_highlight_color"],
                                         bg=theme["button_colors"])

        self.turnOffMixer = tk.Button(self.frame,
                                      text = "\tTurn OFF Mixer",
                                      command=self.mixerOff,
                                      relief="flat",
                                      # image=img4,
                                      compound="left",
                                      highlightcolor=theme["button_highlight_color"],
                                      bg=theme["button_colors"]
                                      )

        self.turnOnMixer = tk.Button(self.frame,
                                     text = "\tTurn ON Mixer",
                                     command = self.mixerOn,
                                     relief="flat",
                                     # image=img4,
                                     compound="left",
                                     highlightcolor=theme["button_highlight_color"],
                                     bg=theme["button_colors"]
                                     )

        self.cleanLabel.grid(row= 0,column =1, padx = 10, pady = 10)
        self.timeMenu.grid(row =0, column =0, padx =10, pady =10)

        self.MotorUpButton.grid(row =1, column = 0, padx =10, pady =10)
        self.motorDownButton.grid(row =1, column = 1, padx = 10, pady =10)

        self.turnOffMixer.grid(row = 2, column = 0, padx = 10, pady = 10)
        self.turnOnMixer.grid(row = 2, column = 1, padx = 10, pady =10)


    def mixerOn(self):
        pass
        # CHECK HERE FOR BUGS, ON 3RD DRINK IT KEPT SPINNING FOREVER!
        # mixer_motor.write(0)  # turns on motor

    def mixerOff(self):
        pass
        # mixer_motor.write(1)

    def motorUp(self):
        pass
        '''
        stepper_motor_dir.write(1)
        for x in range(step_count):
            #         GPIO.output(STEP, GPIO.HIGH)
            stepper_motor_step.write(1)
            t.sleep(delay)
            stepper_motor_step.write(0)
            t.sleep(delay)
        stepper_motor_enable.write(1)
        '''


    def motorDown(self):
        pass
        '''
        stepper_motor_enable.write(0)
        t.sleep(1)
        stepper_motor_dir.write(0)

        for x in range(step_count):
            stepper_motor_step.write(1)
            t.sleep(delay)
            stepper_motor_step.write(0)
            t.sleep(delay)
        '''


    def clean(self):
        pass
'''
            pump1_1.write(0)
            pump1_2.write(0)
            pump1_3.write(0)
            pump1_4.write(0)
            pump1_5.write(0)
            pump1_6.write(0)
            pump1_7.write(0)
            pump1_8.write(0)
#             pump2_1.write(0)
#             pump2_2.write(0)
#             pump2_3.write(0)
#             pump2_4.write(0)
#             pump2_5.write(0)
#             pump2_6.write(0)
#             pump2_7.write(0)
#             pump2_8.write(0
           

            t.sleep(int(self.time.get()))

            pump1_1.write(1)
            pump1_2.write(1)
            pump1_3.write(1)
            pump1_4.write(1)
            pump1_5.write(1)
            pump1_6.write(1)
            pump1_7.write(1)
            pump1_8.write(1)
#             pump2_1.write(1)
#             pump2_2.write(1)
#             pump2_3.write(1)
#             pump2_4.write(1)
#             pump2_5.write(1)
#             pump2_6.write(1)
#             pump2_7.write(1)
#             pump2_8.write(1)
          '''


class mainlayout():
    def __init__(self):
        super(mainlayout, self).__init__()
        # USE THIS CODE FOR LINUX DISTRO
        # self.window.attributes('-zoomed', True)
        self.window = tk.Tk()
        # self.window.geometry('3200x1800')

        # led.colorCupPlacement(strip)

        self.getWindowSize(self.window)

        self.window.title("BBC (Best Bartending Companion")
        self.window.configure(bg = theme["background_color"])
        #USE THIS CODE For Windows distro
        #-zoomed
        self.window.attributes('-fullscreen', True)
        self.fullScreenState = False
        self.window.bind("<F11>",
                         lambda event: self.window.attributes("-fullscreen",
                                                              not self.window.attributes("-fullscreen")))
        self.window.bind("<Escape>",
                         lambda event: self.window.attributes("-fullscreen",
                                                              False))


        #______________________________________________________________________
        if pumps[0] == " ":
            self.newAlcoholWindow()

        self.addlayout()



        self.window.mainloop()

    def getWindowSize(self, window):

        file = open("../data/display.json", "r")
        data = json.load(file)
        file.close()


        x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / data["confirm_scale_x"]
        y = (window.winfo_screenheight() - window.winfo_reqheight()) / data["confirm_scale_y"]

        data["h"] = x
        data["w"] = y
        # data["total_width"] = window.winfo_screenwidth() -100

        file = open("../data/display.json", "w")
        json.dump(data,file,indent=2)
        file.close()

    def addlayout(self):



        img = tk.PhotoImage(file = "../img/menu2.png")
        im2 = tk.PhotoImage(file = "../img/layout.png")
        im2b = im2.subsample(2,2)
        im3 = tk.PhotoImage(file = "../img/create.png")
        im3b = im3.subsample(2,2)
        img4 =tk.PhotoImage(file = "../img/clean.png")


        # PRODUCTION VALUES
        self.menuButton = tk.Button(
            self.window,
            text= "\tMenu",
            command = self.displayMenu,
            relief="flat",
            image = img,
            compound = "left",
            highlightcolor=theme["button_highlight_color"],
            bg=theme["button_colors"],
            height = 400)
        self.menuButton.image = img


        # DEVELOPMENT VALUES
        # self.menuButton = tk.Button(
        #     self.window,
        #     text="\tMenu",
        #     command=self.displayMenu,
        #     relief="flat",
        #     image=img,
        #     compound="left",
        #     highlightcolor=theme["button_highlight_color"],
        #     bg=theme["button_colors"],
        #     height=300)
        # self.menuButton.image = img


        # PRODUCTION VALUES
        self.layoutbutton = tk.Button(
            self.window,
            text="Layout",
            command=self.newAlcoholWindow,
            image = im2b,
            compound = "left",
            relief="flat",
            highlightcolor=theme["button_highlight_color"],
            bg=theme["button_colors"],
            height = 400)
        self.layoutbutton.image = im2b

        # DEVELOPMENT VALUES
        # self.layoutbutton = tk.Button(
        #     self.window,
        #     text="Layout",
        #     command=self.newAlcoholWindow,
        #     image=im2b,
        #     compound="left",
        #     relief="flat",
        #     highlightcolor=theme["button_highlight_color"],
        #     bg=theme["button_colors"],
        #     height=300)
        # self.layoutbutton.image = im2b

        # PRODUCTION VALUES
        self.createButton = tk.Button(self.window,
            text="\tCreate",
            command=self.displayCreateDrink,
            relief="flat",
            image = im3b,
            compound = "left",
            highlightcolor=theme["button_highlight_color"],
            bg=theme["button_colors"])
        self.createButton.image = im3b

        self.cleanButton = tk.Button(self.window,
            text="\tSettings",
            command=self.cleanPumps,
            relief="flat",
            image = img4,
            compound = "left",
            highlightcolor=theme["button_highlight_color"],
            bg=theme["button_colors"])
        self.cleanButton.image = img4

        # PRODUCTION VALUES
        self.menuButton.grid(row = 0, column = 0,padx =30, pady =30,  sticky="nsew")
        self.createButton.grid(row =0, column =1, padx =30, pady =30, sticky="nsew")
        self.layoutbutton.grid(row =2, column = 0, padx =30, pady =30,sticky="nsew")
        self.cleanButton.grid(row=2, column =1, padx = 30, pady =30, sticky="nsew")


        # DEVELOPMENT VALUES
        # self.menuButton.grid(row=0, column=0, padx=30, pady=10, sticky="nsew")
        # self.createButton.grid(row=0, column=1, padx=30, pady=10, sticky="nsew")
        # self.layoutbutton.grid(row=2, column=0, padx=30, pady=10, sticky="nsew")
        # self.cleanButton.grid(row=2, column=1, padx=30, pady=10, sticky="nsew")

        self.window.grid_columnconfigure(0, weight = 1)
        self.window.grid_columnconfigure(1, weight = 1)
        self.window.grid_columnconfigure(1, weight = 1)

    def newAlcoholWindow(self):
        self.alcWindow = tk.Toplevel(self.window)
        self.alcWindow.attributes('-topmost', 'true')
        self.newlayer = alcLayout(self.alcWindow)


    def displayMenu(self):
        self.menuWindow = tk.Toplevel(self.window)
        self.menuWindow.attributes('-topmost', 'true')
        self.menuWindow.configure(bg = "black")
        #USE THIS CODE For Windows distro
        self.menuWindow.attributes('-fullscreen', True)
        self.fullScreenState = True
        self.menuWindow.bind("<F11>",
                         lambda event: self.menuWindow.attributes("-fullscreen",
                                                              not self.menuWindow.attributes("-fullscreen")))
        self.menuWindow.bind("<Escape>",
                         lambda event: self.menuWindow.attributes("-fullscreen",
                                                              False))

        self.menyLayer = menuLayout(self.menuWindow)

    def displayCreateDrink(self):
        pass

    def cleanPumps(self):
        # led.colorWipe(strip, Color(0, 0, 0), 10)
        self.settingsMenu = tk.Toplevel(self.window)
        self.settingsMenu.attributes('-topmost', 'true')
        self.newlayer = settingsLayout(self.settingsMenu)
        time  =3



if __name__ == '__main__':

    mainlayout()