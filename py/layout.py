import tkinter as tk
import json


read = open("../data/display.json", "r")
linedata = json.load(read)
read.close()



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

