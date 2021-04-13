import tkinter as tk
from tkinter import ttk
import time as t
import threading
import asyncio
import json

small_mili = 90
medium_mili = 150
large_mili = 210
shot_mili = 40



read = open("./data/theme.json", "r")
theme = json.load(read)
read.close()


nread = open("./data/recipes.json", "r")
d = json.load(nread)
recipes = d["drinks"]
shotrecipies = d["shot"]
nread.close()


if __name__ == "__main__":
    check_config()


class dispenseLayout():
    def __init__(self, master, content, obj, ratio, dtype):
        self.master = master

        master.title = "Confirm"

        self.done_dispensing = True
        self.frame = tk.Frame(self.master)
        self.frame2 = tk.Frame(self.master)

        self.frame.grid(row=0, padx=60, pady=10, sticky="nsew")
        self.frame2.grid(row=1, padx=60, pady=10, sticky="nsew")

        if dtype == "cock":
            self.setLayout(content, obj, ratio)
        else:
            self.shotsetLayout(content, obj, ratio)

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

    def setLayout(self, content, obj, ratio):

        description = ""
        for y in range(len(content)):
            name = "l" + str(y + 1)
            rname = "l" + str(y + 1) + "r"
            if not isinstance(ratio[rname], str):
                description += "\n" + str(int(ratio[rname] * 100)) + "%   " + content[name].title()
            else:
                description += "\n" + content[name].title()

        self.pictureLabel = tk.Label(
            self.frame,
            image=obj["img"]
        )
        self.pictureLabel.grid(row=0, column=0, padx=10, pady=60, sticky="nsew")

        self.drinkLabel = tk.Label(
            self.frame,
            text=obj["name"] + "\n" + description,
            compound="left"
        )
        self.drinkLabel.grid(row=0, column=1, padx=60, pady=60, sticky="nsew")

        if self.done_dispensing:
            self.smallButton = tk.Button(
                self.frame2,
                text="SMALL",
                command=lambda: self.createloadingwindow(content, ratio, small_mili),
                padx=50,
                pady=30,
                bg=theme["size_button_color"]
            )
            self.mediumButton = tk.Button(
                self.frame2,
                text="MEDIUM",
                command=lambda: self.createloadingwindow(content, ratio, medium_mili),
                padx=90,
                pady=30,
                bg=theme["size_button_color"]
            )
            self.largeButton = tk.Button(
                self.frame2,
                text="LARGE",
                command=lambda: self.createloadingwindow(content, ratio, large_mili),
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
                text="NOT DONE DISPENSING PREVIOUS DRINK",
                padx=50,
                pady=30,
                bg=theme["size_button_color"]
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

    async def findPump(self, pumpdata, i, content, ratio, size):

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

    async def mainLoop(self, content, ratio, size):

        read = open("../data/pumps.json", "r")
        pumpdata = json.load(read)
        read.close()

        pump = []

        for a in content:
            pump.append(self.async_loop.create_task(self.findPump(pumpdata, a, content, ratio, size)))

        await asyncio.wait(pump)

    def buffer_function(self, content, ratio, size):
        # self.setlayout()
        self.async_loop.run_until_complete(self.mainLoop(content, ratio, size))
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
        # CHECK HERE FOR BUGS, ON 3RD DRINK IT KEPT SPINNING FOREVER!
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



        # self.canvas.bind("<Enter>", lambda _: self.canvas.bind_all('<Button-1>', self.on_press), '+')
        # self.canvas.bind("<Leave>", lambda _: self.canvas.unbind_all('<Button-1>'), '+')
        # self.canvas.bind("<Enter>", lambda _: self.canvas.bind_all('<B1-Motion>', self.on_touch_scroll), '+')
        # self.canvas.bind("<Leave>", lambda _: self.canvas.unbind_all('<B1-Motion>'), '+')

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


    # def on_press(self,event):
    #     try:
    #         self.offset_y = event.y_root
    #         if self.scrollposition < 1:
    #             self.scrollposition = 1
    #         elif self.scrollposition > self.canvasheight:
    #             self.scrollposition = self.canvasheight
    #         self.canvas.yview_moveto(self.scrollposition / self.canvasheight)
    #     except:
    #         pass

    # def on_touch_scroll(self,event):
    #     try:
    #         nowy = event.y_root

    #         sectionmoved = 40
    #         if nowy > self.prevy:
    #             event.delta = -sectionmoved
    #         elif nowy < self.prevy:
    #             event.delta = sectionmoved
    #         else:
    #             event.delta = 0
    #         self.prevy = nowy

    #         self.scrollposition += event.delta
    #         self.canvas.yview_moveto(self.scrollposition / self.canvasheight)
    #     except:
    #         pass

    def getLayout(self):

        row = 0
        column = 0
        read = open("./data/display.json", "r")
        linedata = json.load(read)
        read.close()

        read = open("./data/pumps.json", "r")
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

                    content = recipes[y+x]["content"]
                    ratio = recipes[y+x]["ratio"]
                    values = {
                        "name":recipes[y+x]["name"],
                        "count":row,
                        "column": column
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
                            break

                    if flag is False:
                        continue

                    if not shotrecipies[y + x]["img"] or shotrecipies[y + x]["img"] == " ":
                        img = tk.PhotoImage(file="./img/default.png")
                    else:
                        # img = tk.PhotoImage(file="img/default.png")
                        img = tk.PhotoImage(file="./img/"+str(recipes[y + x]["img"]))

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

        read = open("./data/display.json", "r")
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

        file = open("./data/display.json", "r")
        data = json.load(file)
        file.close()

        posH = data["h"]
        posw = data["w"]

        self.dispenseMenu.geometry("+%d+%d"%(posH, posw))
        dispenseLayout(self.dispenseMenu,content,obj,ratio, wildcard)


