import tkinter as tk
import json as json
import pyfirmata
settings = __import__("settings")
layout_file = __import__("layout")
menu = __import__("menu")
led = __import__("LED")
# import RPi.GPIO as GPIO



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




read = open("./data/theme.json", "r")
theme = json.load(read)
read.close()


class mainlayout():
    def __init__(self):
        super(mainlayout, self).__init__()
        # self.init_pumps()
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

        self.addlayout()



        self.window.mainloop()

    def getWindowSize(self, window):

        file = open("./data/display.json", "r")
        data = json.load(file)
        file.close()


        x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / data["confirm_scale_x"]
        y = (window.winfo_screenheight() - window.winfo_reqheight()) / data["confirm_scale_y"]

        data["h"] = x
        data["w"] = y
        # data["total_width"] = window.winfo_screenwidth() -100

        file = open("./data/display.json", "w")
        json.dump(data,file,indent=2)
        file.close()

    def addlayout(self):



        img = tk.PhotoImage(file = "./img/menu2.png")
        im2 = tk.PhotoImage(file = "./img/layout.png")
        im2b = im2.subsample(2,2)
        im3 = tk.PhotoImage(file = "./img/create.png")
        im3b = im3.subsample(2,2)
        img4 =tk.PhotoImage(file = "./img/clean.png")


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
        self.newlayer = layout_file.alcLayout(self.alcWindow)


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

        self.menyLayer = menu.menuLayout(self.menuWindow)

    def displayCreateDrink(self):
        pass

    def cleanPumps(self):
        # led.colorWipe(strip, Color(0, 0, 0), 10)
        self.settingsMenu = tk.Toplevel(self.window)
        self.settingsMenu.attributes('-topmost', 'true')
        self.newlayer = settings.settingsLayout(self.settingsMenu)
        time  =3

    '''
    def initPumps(self):
        # intializing arduino board/usb to a variable
        # 
        
        #AUTO CHECKING IF PUMP IS PLUGGED IN (TEST)
        # flag = True
        # x =0
        # board = []
        # while flag: 
        #     usb = "/dev/ttyUSB" + str(x)
        #     try:
        #         board[x] = pyfirmata.Arduino(usb)
        #     except:
        #         flag = False
        # 
        # y =0
        # z =2
        # pumplayout = []
        # for x in board[x]:
        #     pin = "d:" + str(z) + ":o"
        #     z+=1
        #     for r in range(7)
        #     pumplayout[r] = x.get_pin(pin)
            
            # board0 = arduino inside main station
            board0 = pyfirmata.Arduino('/dev/ttyUSB0')
            # board1 = pump station 1
            board1 = pyfirmata.Arduino('/dev/ttyUSB1')
            # board2 = pump station 2
            board2 = pyfirmata.Arduino('/dev/ttyUSB2')
        
        ####Intializing arduino pin to a variable. ex. pump1_3 = pump station #1 pump#3
        
        # pump station 1
        pump1_1 = board1.get_pin('d:2:o')
        pump1_2 = board1.get_pin('d:3:o')
        pump1_3 = board1.get_pin('d:4:o')
        pump1_4 = board1.get_pin('d:5:o')
        pump1_5 = board1.get_pin('d:6:o')
        pump1_6 = board1.get_pin('d:7:o')
        pump1_7 = board1.get_pin('d:8:o')
        pump1_8 = board1.get_pin('d:9:o')
        
        # pump station 2
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
        
        # makes sure pumps are off (1 = "OFF" specifically for the pumps)
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
        
        # makes sure mixer motor is off
        mixer_motor.write(1)
        stepper_motor_enable.write(0)
        
        # Values to control stepper motor
        step_count = 1950  # length of up and down
        delay = .0005  # speed of up and down
    '''

if __name__ == '__main__':

    mainlayout()