from os import name, truncate
from django.db import models
import string
import random
import json
import time as t
import threading
import asyncio
import json

# Create your models here.
#PUT MOST OF YOUR LOGIC IN THE MODEL
#FATMODELS THIN VIEWS


#ARE THOSE GLOBAL VARIABLES HOLDING THE CUP SIZES? YOU NAUGHTY BOY
small_mili = 90
medium_mili = 150
large_mili = 210
shot_mili = 40



def insertPins():
   # DETECT HOW MANY BOXES WE HAVE SETUP 

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

    for x in range(16):
        temp = pumps


def generate_unique_code():
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.objects.filter(code=code).count() == 0:
            break

    return code

# Create your models here.


class Room(models.Model):
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

class Ingredient_id(models.Model):

    width = 400
    height=500
   
    ingredient_id = models.IntegerField(primary_key=True, unique= True)
    ingredient= models.CharField(max_length=50, unique=True)
    pump_picture = models.ImageField(upload_to = "../../img", default = "../../img/default.png", width_field= width, height_field=height)

class pumps(models.Model):
    
    #JUST PULL DATA FROM DATABASE ON WHATS IN THE PUMPS, WE NEED TO BE ABLE TO INSERT THEM INTO THE DATABASE, SO BUILD OUT ROUTING TO FRONT END.
    pump = models.IntegerField(primary_key = True, unique=True)
    ingredient_id = models.CharField(max_length = 100)
    pump_id = models.IntegerField()
    volume_left = models.IntegerField()



    def get_pumps(self, request, format = None):
        print("were in get_pumps")
        pump_components = pumps.objects.all()

        pump_data = PumpSerializer(pump_components, many=True)

        return pump_data
    
    def update_pumps(self, request, format = None): 

        #we may have to format the request object holding the pump data, it depends how the front end sends it. 
        pump_components = pumps.objects.all()
        pump_components = request
        pump_components.save()
        
    


class display(models.Model):
    #THIS IS FOR LATER FOR STYLING IF WE NEED THIS
    color = models.CharField(max_length=50, unique=True)
    drinks_per_row = models.IntegerField()
  

class menu(models.Model):
    
    # nread = open("../../data/recipes.json", "r")
    # d = json.load(nread)
    # recipes = d["drinks"]
    # shotrecipies = d["shot"]
    # nread.close()
    width = 400 
    height =400

    id = models.IntegerField(primary_key =True, unique=True)
    name = models.CharField(max_length=50, unique=True)
    creator_id = models.CharField(max_length=20, default="BBC")
    type_id = models.CharField(max_length=2)
    picture = models.ImageField(upload_to = "../../img/", default= "../../img/cocktail_PNG173.png", width_field = width, height_field=height)

    def buildObject(self,data):
        #3)Graab name of all recipies that make it through the filter
        #4) Build an object to send to the front end. 

        #print(data)
        idx =0
        menu_data = {
            "C":[],
            "S":[],
            "CS":[]
        }

        for x in data:
            name_array = {
                "name": "",
                "creator_id": "",
                "type_id": "",
                "ingredients":{}
            }
            name = menu.objects.values('name','creator_id', 'type_id').filter(id=x)
            temp = ratio.objects.values('ingredient','amount').filter(menu_id=x)
            
            type_id = name[0]['type_id']

            name_array['name'] = name[0]['name']
            name_array['creator_id'] = name[0]['creator_id']
            name_array['type_id'] = name[0]['type_id']
            name_array['ingredients']  = temp[0]
            
            if type_id == "C":
                menu_data["C"].append(name_array)
            elif type_id == "S":
                menu_data["S"].append(name_array)
            elif type_id == "CS":
                menu_data["CS"].append(name_array)

        return menu_data

    def get_menu(self):
        """
            Goal
                1) Grab all menu items that have ingredients in common with the pump list
                2) Filter out any Recipies that dont contain all the ingredients in the pump list
                    ex 
                        Rum and Coke [Rum,Coke]
                        Pumps [Vodka, Rum]
                        filter out Rum and Coke because it contains Coke
                3)Graab name of all recipies that make it through the filter
                4) Build an object to send to the front end. 
        """
        
        pump_components = pumps.objects.values('ingredient_id')
        pump_list = []
        #pump_data = IngredientSerializer(pump_components)
        data = []


        ingredients_list = {}
        
        size =0

        grab = []
        #1) Grab all menu items that have ingredients in common with the pump list
        for x in pump_components:
            #print(x['ingredient_id'])
            #FIRST GRAB ALL MENU_ID'S THAT HAS THAT INGREDIENT IN COMMON WITH X
            if x['ingredient_id'] != '' :
                pump_list.append(x['ingredient_id'])
                
                temp = (ratio.objects.values('menu_id').filter(ingredient=x['ingredient_id']))
                #GRABBING ALL RECIPE ID'S THAT HAVE A INGREDIENT IN COMMON WITH PUMP LIST
                for y in temp:
                    if y['menu_id'] not in grab:
                        grab.append(y['menu_id'])

        #now I have all the menu ID's that contain the ingredients in the ingredients list
        bad_list = []

        #2) Filter out any Recipies that dont contain all the ingredients in the pump list
        for x in grab: 
            temp = ratio.objects.values('ingredient','amount').filter(menu_id=x)
            for y in temp: 
                #print(y)
                if type(y['amount']) is float or type(y['amount']) is int:
                    if y['ingredient'] not in pump_list:
                        if x not in bad_list:
                            bad_list.append(x)
                
        #getting the difference of the 2 lists to grab all the good data. 
        diff_list1_list2 = set(bad_list) - set(grab)
        diff_list2_list1 = set(grab) - set(bad_list)
        data = list(diff_list1_list2) + list(diff_list2_list1)

      
        menu_data = self.buildObject(data)

        return menu_data

class board_object:
    def __init__(self, station, pin):
        self.station = station
        self.pin = pin

class settings():
    '''
    # Values to control stepper motor
    step_count = 1950  # length of up and down
    delay = .0005  # speed of up and down
          
    board_list = []
    pump_list = [
        station[]
    ]
    for x in range(10):
        try:
            file_path = '/dev/ttyUSB' + str(x)
            board_list[x] = pyfirmata.Arduino(file_path)
        except:
            break

    # board0 = arduino inside main station
    #board0 = pyfirmata.Arduino('/dev/ttyUSB0')
    # board1 = pump station 1
    #board1 = pyfirmata.Arduino('/dev/ttyUSB1')
    # board2 = pump station 2
    #board2 = pyfirmata.Arduino('/dev/ttyUSB2')
        
    ####Intializing arduino pin to a variable. ex. pump1_3 = pump station #1 pump#3
    for x in board_list:
        pump_list.append(board_object())

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

    def get_stations():


    def mixer_up():
        pass
    #     stepper_motor_dir.write(1)
    #     for x in range(step_count):
    # #         GPIO.output(STEP, GPIO.HIGH)
    #         stepper_motor_step.write(1)
    #         t.sleep(delay)
    #         stepper_motor_step.write(0)
    #         t.sleep(delay)
    #     stepper_motor_enable.write(1)

    def mixer_down(self):
        pass
        # stepper_motor_dir.write(0)
        #
        # for x in range(step_count):
        #     stepper_motor_step.write(1)
        #     t.sleep(delay)
        #     stepper_motor_step.write(0)
        #     t.sleep(delay)

    def led_off():
        pass
    def led_on():
        pass

    def clean_pump():

  
class ratio(models.Model):
    menu_id= models.IntegerField()
    ingredient = models.CharField(max_length=50)
    amount = models.IntegerField()
    total_ingredients = models.IntegerField()


class confirm():

    def confirm(self, request, format = None):
        '''

            DATA WE ARE WORKING WITH:
                small_mili = 90
                medium_mili = 150
                large_mili = 210
                shot_mili = 40

            HERE IS WHERE WE WILL EXECUTE THE PUMP CODE.
            GOALS:
                1) GET A BAEFY
                2) GRAB ALL PUMP INGREDIENTS
                3) GRAB FROM THE FRONT END THE INGREDIENTS AND SIZE OF CUP
                4) GRAB THE RECIPE FROM THE BACKEND AND RATIO IN SHIT
                5) CREATE A LIST OF ALL THE PUMPS THAT NEED TO BE TURNED ON 
                6) CALCULATE HOW LONG THE PUMPS NEED TO RUN BASED ON SIZE OF CUP 
                7) EXECUTE IT ASYNCHRONOUSLY (FUUUUUUUCCKKKKK)
                
                EXTRA CREDIT ;):
                    1) GET THEM LED'S FOOKIN WORKING AMRIGHT


            OLD CODE
                1) WE THREADED THE PUMPS DUE TO THE GUI NOT WORKING WHILE THE PUMPS RAN. WE MAY NOT NEED TO DO THAT SINCE WE ARE RUNNING A WEBSERVER (def createloadingwindow)
                2) WE THEN WENT TO A BUFFER FUNTION, THIS FUNCTION ADDED OUR TASK (DISPENSING PUMPS) TO THE LIST/ARRAY OF WORK WE NEEDED TO GET DONE. EACH PUMP THAT WE NEEDED GOT ADDED TO THE LIST. 
                3) WE THEN BEGAN THE WORK OF FIND OUT WHICH PUMP HAD WHICH INGREDIENT AND THEN TELLING THAT PUMP TO TURN ON. 
        '''

        #1. BAEFY SECURED, MOVING OUT
        pump_list = []

        #2. GRAB ALL THE PUMP INGREDIENTS
        pump_components2 = pumps.objects.values('pump','ingredient_id')
    
        y=0
        for x in pump_components2:
           print(x['pump'])
           print(x['ingredient_id'])


        #3) GRAB FROM THE FRONT END THE INGREDIENTS AND size 
        '''
            HOPEFULLY WE CAN CREATE THE DATA SO ITS INTHE FORMAT OF 
            ingredients:[
                'vodka': .10,
                'rum' : .20
            ]

            IF NOT I AM JUST GOING TO GRAB THE RECIPE FROM THE BACKEND WITH THE INGREDIENT ID AHUKE
        '''

        #work on this not sure if this will work sadly lmao roflcopter
        recipe_id = request.POST.get('menu_id')
        size = request.POST.get('size')


        #4) GRAB THE RECIPE FROM THE BACKEND AND RATIO IN SHIT
        drinkOBJ = (ratio.objects.values('amount','ingredient').filter(menu_id=recipe_id))

        #5) CREATE A LIST OF ALL THE PUMPS THAT NEED TO BE TURNED ON 
        for x in drinkOBJ: 
            for y in pump_components2:
                if x['ingredient'] == y["ingredient_id"]:
                    pump_list.append(y["pump"])

        print(pump_list)
   
        return self.buffer_function(pump_list, drinkOBJ['amount'],size)
      

    def buffer_function(self, pump_list, ratio, size):
        # self.setlayout()
        self.async_loop.run_until_complete(self.mainLoop(pump_list, ratio, size))
        print("test")
        # stepper_motor_enable.write(0)
        # t.sleep(1)
        # self.down()
        # t.sleep(1)
        # self.spinMotor()
        # t.sleep(1)
        # self.up()


        #5) CALCULATE HOW LONG THE PUMPS NEED TO RUN BASED ON SIZE OF CUP
        '''
            DATA WE ARE WORKING WITH:
             size =    small_mili = 90
             size =    medium_mili = 150
             size =    large_mili = 210
              size =   shot_mili = 40
                
                ratio = .3 out of 1 or 1/3
            
            formula: time = (ratio * size) / 3

            I cant remember why we are diving by 3 but well figure it out when we test LOL
        '''
      

    async def findPump(self, pump, ratio, size):

        time = (ratio * size) / 3
        z = ""
        for x in pump:
            if x == 1:
                pump1.write(0)
                pump1_1.write(0)
                await asyncio.sleep(time)
                pump1_1.write(1)
                
    
    async def mainLoop(self, pump_list, ratio, size):

        for a in pump_list:
            pump.append(self.async_loop.create_task(self.findPump(a, ratio, size)))

        await asyncio.wait(pump)



    
'''
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



'''




  