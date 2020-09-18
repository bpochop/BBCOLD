import tkinter as tk
import json as json
from tkinter import ttk, messagebox
# import RPi.GPIO as GPIO
import pyfirmata as pyfirm
import asyncio
import time as t
import threading

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
shot_mili = 45




DIR = 20   # Direction GPIO Pin#
STEP = 21  # Step GPIO Pin#
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 48   # Steps per Revolution (360 / 7.5) ***will need to test the right amount later

# GPIO.setmode(GPIO.BCM) #sets GPIO numbers instead of the board number
# GPIO.setup(DIR, GPIO.OUT) #gpio pin assigned as an output
# GPIO.setup(STEP, GPIO.OUT)
#
# GPIO.output(DIR, CW) #this sets the first rotation. clockwise = going down

step_count = SPR
delay = .500 #this will control the speed of the motor *** will need to test later for right speed




nread = open("pumps.json", "r")
d = json.load(nread)
pumps = []
for x in d:
    pumps.append(d[x])
nread.close()

nread = open("recipes.json", "r")
d = json.load(nread)
recipes = d["drinks"]
shotrecipies = d["shot"]
nread.close()

read = open("display.json", "r")
linedata = json.load(read)
read.close()


read = open("theme.json", "r")
theme = json.load(read)
read.close()

#intializing arduino board/usb to a variable
#board1 = pump station 1
# board1 = pyfirm.Arduino('COM4') #this "COM4" address will change on the pi
#                                    #will check new address later
#
# board2 = pyfirm.Arduino('COM5')
#
# # # Intializing arduino pin to a variable. ex. pump1_3 = pump station #1 pump#3
# #
# # #pump station 1
# pump1_1 = board1.get_pin('d:2:o')
# pump1_2 = board1.get_pin('d:3:o')
# pump1_3 = board1.get_pin('d:4:o')
# pump1_4 = board1.get_pin('d:5:o')
# pump1_5 = board1.get_pin('d:6:o')
# pump1_6 = board1.get_pin('d:7:o')
# pump1_7 = board1.get_pin('d:8:o')
# pump1_8 = board1.get_pin('d:9:o')
#
# #pump station 2
# pump2_1 = board2.get_pin('d:2:o')
# pump2_2 = board2.get_pin('d:3:o')
# pump2_3 = board2.get_pin('d:4:o')
# pump2_4 = board2.get_pin('d:5:o')
# pump2_5 = board2.get_pin('d:6:o')
# pump2_6 = board2.get_pin('d:7:o')
# pump2_7 = board2.get_pin('d:8:o')
# pump2_8 = board2.get_pin('d:9:o')
#
# #makes sure pumps are off
# pump1_1.write(0)
# pump1_2.write(0)
# pump1_3.write(0)
# pump1_4.write(0)
# pump1_5.write(0)
# pump1_6.write(0)
# pump1_7.write(0)
# pump1_8.write(0)
# pump2_1.write(0)
# pump2_2.write(0)
# pump2_3.write(0)
# pump2_4.write(0)
# pump2_5.write(0)
# pump2_6.write(0)
# pump2_7.write(0)
# pump2_8.write(0)
#
#



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

        # self.loop = asyncio.get_event_loop()
        threading.Thread(target=self.buffer_function, args=(content, ratio, dtype)).start()
        # self.loop.close()
        elapsed = t.perf_counter() - s
        print(f"{__file__} executed in {elapsed:0.2f} seconds.")


        self.master.destroy()


    def spinMotor(self):
        pass
        # motorMix = 16
        # GPIO.setup(motorMix, GPIO.OUT)
        #
        # GPIO.output(motorMix, GPIO.HIGH)  # runs motor
        # t.sleep(3)  # runs for 3 seconds
        # GPIO.output(motorMix, GPIO.LOW)  # turns off motor

    async def findPump(self,pumpdata, i, content, ratio, size):


        time = (ratio[i + "r"] * size) / 10
        z = ""
        for x in pumpdata:
            if content[i].title() in pumpdata[x]:

                z = x

                if z == "pump1_1":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp1_1 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break
                if z == "pump1_2":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp1_2 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break
                if z == "pump1_3":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp1_3 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break
                if z == "pump1_4":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp1_4 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break
                if z == "pump1_5":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp1_5 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break
                if z == "pump1_6":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp1_6 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break
                if z == "pump1_7":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp1_7 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break
                if z == "pump1_8":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp1_8 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break
                if z == "pump2_1":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp2_1 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break
                if z == "pump2_2":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp2_2 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    # name.write(0)
                    break
                if z == "pump2_3":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp2_3 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break
                if z == "pump2_4":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp2_4 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break
                if z == "pump2_5":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp2_5 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break
                if z == "pump2_6":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp2_6 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break
                if z == "pump2_7":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp2_7 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break
                if z == "pump2_8":
                    # name.write(1)

                    s = t.perf_counter()
                    print(time)
                    await asyncio.sleep(time)
                    elapsed = t.perf_counter() - s
                    print(f"PUmp2_8 executed in {elapsed:0.2f} seconds.")
                    # name.write(0)
                    break




    async def mainLoop(self,content, ratio,size):

        read = open("pumps.json", "r")
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
        # for x in range(step_count):  # this will run down for # length depending on SPR
        #     GPIO.output(STEP, GPIO.HIGH)
        #     t.sleep(delay)
        #     GPIO.output(STEP, GPIO.LOW)
        #     t.sleep(delay)
        #
        # # im not sure how to simultanousely call the motor that mixes
        # self.spinMotor()
        #
        # t.sleep(3)  # time delay before it goes up, while motor mixes
        #
        # GPIO.output(DIR, CCW)  # now it will be counterclockwise/will go up
        # for x in range(step_count):
        #     GPIO.output(STEP, GPIO.HIGH)
        #     t.sleep(delay)
        #     GPIO.output(STEP, GPIO.LOW)
        #     t.sleep(delay)
        #
        # GPIO.cleanup()  # cleans up gpio pin back to input to prevent damage for next time use
        #

        self.done_dispensing = True





class menuLayout():
    def __init__(self, master):

        self.master = master

        try:
            self.style = ttk.Style()

            color1 = theme["tab_color1"]
            color2 = theme["tab_color2"]

            self.style.theme_create("yummy", parent="alt", settings={
                "TNotebook": {"configure": {"tabmargins": [25, 5, 2, 0], "background": "black"}, "orient": "vertical"},
                "TNotebook.Tab": {
                    "configure": {"padding": [250, 25], "background": color1},
                    "map": {"background": [("selected", color2)],
                            "expand": [("selected", [1, 1, 1, 0])]}}})

            self.style.theme_use("yummy")
        except:
            self.style.theme_use("yummy")

        master.title = "DRINK MENU"

        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(side="left", fill="both", expand=1)

        self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side = "right", fill ="y",expand=0)

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.canvasheight = 2000

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(self.canvas, height=self.canvasheight, bg="black")
        self.interior_id = self.canvas.create_window(0, 0, window=interior, anchor="nw")

        self.interior.bind('<Configure>', self._configure_interior)

        self.canvas.bind('<Configure>', self._configure_canvas)



        self.canvas.configure(yscrollcommand =self.scrollbar.set,bg = "black")
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
        # self.tablayout.config(orient = "vetical")

        self.drinkTab = tk.Frame(self.tablayout, bg = "black")
        self.shotTab = tk.Frame(self.tablayout, bg = "black")
        self.backTab = tk.Frame(self.tablayout)

        self.backTab.bind("<Visibility>",lambda e: self.killitall())
        self.tablayout.add(self.drinkTab, text = "Drinks")
        self.tablayout.add(self.shotTab, text = "Shots")
        self.tablayout.add(self.backTab, text="Back")

        # self.frame2 = tk.Frame(self.canvas)
        # self.frame2.configure(bg = "black")

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
        read = open("display.json", "r")
        linedata = json.load(read)
        read.close()

        read = open("pumps.json", "r")
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
                        img = tk.PhotoImage(file="img/default.png")
                    else:
                        # img = tk.PhotoImage(file="img/default.png")
                        img = tk.PhotoImage(file=str(recipes[y + x]["img"]))

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
                        img = tk.PhotoImage(file="img/default.png")
                    else:
                        # img = tk.PhotoImage(file="img/default.png")
                        img = tk.PhotoImage(file=str(recipes[y + x]["img"]))

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


        description = obj['name'] + "\n"


        for y in range(len(content)):
            name = "l" + str(y + 1)
            description += "\n"+ content[name].title()

        self.button1 = tk.Button(
            tab,
            text=description,
            relief="flat",
            image = obj["img"],
            compound="left",
            highlightcolor=theme["button_highlight_color"],
            bg=theme["button_colors"],
            padx = 20,
            command = lambda :self.createDispenseMenu(content, obj,ratio, wildcard),
            )
        self.button1.image = obj["img"]
        self.button1.grid(row=obj["count"], column=obj["column"], padx=width, pady=(20,height), sticky="nsew")

    def createDispenseMenu(self,content,obj,ratio,wildcard):

        self.dispenseMenu = tk.Toplevel(self.tablayout)
        self.dispenseMenu.attributes('-topmost', 'true')
        self.dispenseMenu.configure(bg='#f0f0f0')
        ##40E0D0

        file = open("display.json", "r")
        data = json.load(file)
        file.close()

        posH = data["h"]
        posw = data["w"]

        self.dispenseMenu.geometry("+%d+%d"%(posH, posw))
        dispenseLayout(self.dispenseMenu,content,obj,ratio, wildcard)





class alcLayout():
    def __init__(self, master):
        self.master = master
        nread = open("pumps.json", "r")
        d = json.load(nread)
        self.pumps = []
        for x in d:
            self.pumps.append(d[x])

        self.frame = tk.Frame(master)
        master.title = "Set Layout"
        self.getLayout()

        # Readin JSON data and check if there are any saved loadout configurations


    def getLayout(self):

        read = open("drinks.json", "r")
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
        descriptionLabel = tk.Label(self.frame,text = "Drinks per Line",justify = "left")

        self.displaychoices = tk.StringVar(self.frame)
        self.displaychoices.set(linedata["display"])
        self.displaymenu = tk.OptionMenu(self.frame, self.displaychoices, *self.display)
        self.displaymenu.grid(row =18, column =1)
        descriptionLabel.grid(row=18, column =0)

        self.frame.pack()


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

        read = open("pumps.json", "r")
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

        write = open("pumps.json", "w")
        json.dump(drinkdata, write, indent=2)
        write.close()

        write = open("display.json", "w")
        json.dump(linedata, write, indent=2)
        write.close()

        self.master.destroy()





class mainlayout():
    def __init__(self):
        super(mainlayout, self).__init__()
        # USE THIS CODE FOR LINUX DISTRO
        # self.window.attributes('-zoomed', True)

        self.window = tk.Tk()

        self.getWindowSize(self.window)

        self.window.title("BBC (Best Bartending Companion")
        self.window.configure(bg = "black")
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

        file = open("display.json", "r")
        data = json.load(file)
        file.close()

        x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / data["confirm_scale_x"]
        y = (window.winfo_screenheight() - window.winfo_reqheight()) / data["confirm_scale_y"]

        data["h"] = x
        data["w"] = y
        # data["total_width"] = window.winfo_screenwidth() -100

        file = open("display.json", "w")
        json.dump(data,file,indent=2)
        file.close()



    def addlayout(self):



        img = tk.PhotoImage(file = "img/menu2.png")
        im2 = tk.PhotoImage(file = "img/layout.png")
        im2b = im2.subsample(2,2)
        im3 = tk.PhotoImage(file = "img/create.png")
        im3b = im3.subsample(2,2)


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
            text="\tClean",
            # command=self.displayCreateDrink,
            relief="flat",
            image = im3b,
            compound = "left",
            highlightcolor=theme["button_highlight_color"],
            bg=theme["button_colors"])

        self.menuButton.grid(row = 0, column = 0,padx =30, pady =30,  sticky="nsew")
        self.createButton.grid(row =0, column =1, padx =30, pady =30, sticky="nsew")
        self.layoutbutton.grid(row =2, column = 0, padx =30, pady =30,sticky="nsew")
        self.cleanButton.grid(row=2, column =1, padx = 30, pady =30, sticky="nsew")

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
        self.fullScreenState = False
        self.menuWindow.bind("<F11>",
                         lambda event: self.menuWindow.attributes("-fullscreen",
                                                              not self.menuWindow.attributes("-fullscreen")))
        self.menuWindow.bind("<Escape>",
                         lambda event: self.menuWindow.attributes("-fullscreen",
                                                              False))

        self.menyLayer = menuLayout(self.menuWindow)

    def displayCreateDrink(self):
        pass





if __name__ == '__main__':

    mainlayout()