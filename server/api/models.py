from os import name, truncate
from django.db import models
import string
import random
import json
import time as t
import threading
import asyncio
import json
import pyfirmata

# Create your models here.
#PUT MOST OF YOUR LOGIC IN THE MODEL
#FATMODELS THIN VIEWS


#ARE THOSE GLOBAL VARIABLES HOLDING THE CUP SIZES? YOU NAUGHTY BOY
small_mili = 90
medium_mili = 150
large_mili = 210
shot_mili = 40

step_count = 1900  # length of up and down
delay = .0005  # speed of up and down
clean_time = 5    
spin_time = 3

pump_list = []
board0 = pyfirmata.Arduino('/dev/ttyUSB0')
####Initializing arduino pin for the steppper motor inside main station
stepper_motor_dir = board0.get_pin('d:2:o')
stepper_motor_step = board0.get_pin('d:3:o')
stepper_motor_enable = board0.get_pin('d:7:o')
mixer_motor = board0.get_pin('d:4:o')

drink_in_progress = False


mixer_motor.write(1)
stepper_motor_enable.write(0)

def check_drink_inprogress():
    print("TESTING FOR DRINK")
    print(drink_in_progress)
    if drink_in_progress == True:
        return True
    else:
        return False

def change_progress(progress):
    drink_in_progress = progress
    

def check_config():
    if len(pump_list) == 0:
        get_stations()



def get_stations():
        
    board_list = []
    #  board0 = arduino inside main station
    
    #We start at 1 because board0 is reserved for the main board, this board is not inside of a pump
    for x in range(1,10):
        try:
            file_path = '/dev/ttyUSB' + str(x)
            board_list.append(pyfirmata.Arduino(file_path))
        except:
            break
    

    ####Intializing arduino pin to a variable. ex. pump1_3 = pump station #1 pump#3
    for x in board_list:
        #x = board1, board2
        for y in range(2,10):
            #pin = d:2:0, d:3:o
            pin = 'd:' +str(y) +':o' 
            # x.get_pin = board1.getpin, board2.getpin
            pump_list.append(x.get_pin(pin))
            

    # makes sure pumps are off (1 = "OFF" specifically for the pumps)
    for x in pump_list:
        x.write(1)

    

    '''
        Here we are Cleaning up the database if they remove/add a pump

        1) Get pump database size
        2) if sum of arduino pumps are greater then database size pumps remove excess
        ^
        Im guessing this one wont be used much, but it might help us troubleshoot later. 
        3) if sum of arduino pumps are less then database size then add extra pumps to the database.

    '''

    #1)
    pump_size = pumps()
    db_size = pump_size.objects.count()
    actual_pumps = pump_list.len()

    #2)
    if actual_pumps < db_size:
        
        #get the difference in pumps i.e db_size = 16 acutal_pumps = 8; size = 8
        x = db_size - actual_pumps
        
        #then from 8 -> 16 we are deleting the excess database objects
        for i in range(x,db_size):
            temp = pump_size.object.get(pump = i)
            temp.delete()
    #3)
    elif actual_pumps > db_size: 
        #get the difference in pumps i.e db_size = 8 acutal_pumps = 16; size = 8
        x = actual_pumps - db_size

        #then from 8 -> 16 we are adding the extra database objects
        for i in range(x, actual_pumps):
            new_entry = pumps(id=i+1)
            new_entry.save()



# Create your models here.


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
        get_stationspump_components = request.data
        pump_components.save()
        
    


class display(models.Model):
    #THIS IS FOR LATER FOR STYLING IF WE NEED THIS
    color = models.CharField(max_length=50, unique=True)
    drinks_per_row = models.IntegerField()
  

class menu(models.Model):
    
    width = "400"
    height = "400"

    id = models.IntegerField(primary_key =True, unique=True)
    name = models.CharField(max_length=50, unique=True)
    creator_id = models.CharField(max_length=20, default="BBC")
    type_id = models.CharField(max_length=2)
    picture = models.ImageField(upload_to = "../../img/", default= "../../img/cocktail_PNG173.png")

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
                "ingredients":{},
                "picture": ""
            }
            name = menu.objects.values('name','creator_id', 'type_id', 'picture').filter(id=x)
            temp = ratio.objects.values('ingredient','amount').filter(menu_id=x)
            
            type_id = name[0]['type_id']

            name_array['name'] = name[0]['name']
            name_array['creator_id'] = name[0]['creator_id']
            name_array['type_id'] = name[0]['type_id']
            name_array['ingredients']  = temp[0]
            name_array['picture'] = name[0]['picture']
            
            if type_id == "C":
                menu_data["C"].append(name_array)
            elif type_id == "S":
                menu_data["S"].append(name_array)
            elif type_id == "CS":
                menu_data["CS"].append(name_array)
        print(menu_data)
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
    
    def create_drink(self, data):
        '''
            1) Grab last id inserted into database
            2) Increase Id
            3) create new Object for table
            4) Save
        '''
        
        last_id = int(menu.objects.values('id').last())
        last_id = last_id + 1
        
        new_entry = menu(id=last_id, name= data['name'], type_id=data['type'])
        new_entry.save()




class settings():

    def mixer_up(self):

        #DIRECTION
        stepper_motor_dir.write(1)
    
   
        for x in range(step_count):
            #we are enabling the motor
            stepper_motor_enable.write(0)
            stepper_motor_step.write(1)         #turning on the motor
            t.sleep(delay)
            stepper_motor_step.write(0)         #turning on the motor
            t.sleep(delay)
        stepper_motor_enable.write(1)           #abosolutly making sure the motor is off
       
    def mixer_down(self):

        #DIRECTION
        stepper_motor_dir.write(0)
   
        
        for x in range(step_count):
            #GPIO.output(STEP, GPIO.HIGH)
            stepper_motor_enable.write(0)
            stepper_motor_step.write(1)
            t.sleep(delay)
            stepper_motor_step.write(0)
            t.sleep(delay)

        t.sleep()
    

    def led_off(self):
        pass
    def led_on(self):
        pass

    def clean_pump(self):
        split = len(pump_list)

        for x in range(split):
            print(x)
            if (x%7 ==0 and x != 0):
                print("we in the check")
                t.sleep(clean_time)
                print("sleepy sleepy")
                for y in range(x):
                    pump_list[y].write(1) #off?
            
            pump_list[x].write(0) #on?

        #make sure its super off lmao
        for x in range(split):
            pump_list[x].write(1)

    def detect_Pumps(self):
        #this should redo the Pumps detection
        get_stations()


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
        temp_pump_list = []
        change_progress(True)

        #2. GRAB ALL THE PUMP INGREDIENTS
        pump_components2 = pumps.objects.values('pump','ingredient_id')
    
        y=0
        # for x in pump_components2:
        #    print(x['pump'])
        #    print(x['ingredient_id'])


        #3) GRAB FROM THE FRONT END THE INGREDIENTS AND size 
        '''
            HOPEFULLY WE CAN CREATE THE DATA SO ITS INTHE FORMAT OF 
            ingredients:[
                'vodka': .10,
                'rum' : .20
            ]

        '''


        #ADJUST THIS ONCE FRONT END GETS DONE!

        size = request['size']

        for x in request['ingredients']:
            for y in pump_components2:
                if x == y['ingredient_id']
                    temp_pump_list.append(y["pump"])
                    
    
        self.buffer_function(temp_pump_list, request,size)
        return change_progress(False)
        

    async def down(self):
         #DIRECTION
        stepper_motor_dir.write(0)
   
        
        for x in range(step_count):
            #GPIO.output(STEP, GPIO.HIGH)
            stepper_motor_enable.write(0)
            stepper_motor_step.write(1)
            await asyncio.sleep(delay)
            stepper_motor_step.write(0)
            await asyncio.sleep(delay)
    
    def up(self):
        #DIRECTION
        stepper_motor_dir.write(1)
    
   
        for x in range(step_count):
            #we are enabling the motor
            stepper_motor_enable.write(0)
            stepper_motor_step.write(1)         #turning on the motor
            t.sleep(delay)
            stepper_motor_step.write(0)         #turning on the motor
            t.sleep(delay)
        stepper_motor_enable.write(1)           #abosolutly making sure the motor is off  
      
    def spinMotor(self):
        # CHECK HERE FOR BUGS, ON 3RD DRINK IT KEPT SPINNING FOREVER!
        mixer_motor.write(0)# turns on motor
        t.sleep(5) #BUG HERE MAYBE? DIDNT WAKE UP
        mixer_motor.write(1)

    def buffer_function(self, temp_pump_list, ratio, size):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.async_loop = asyncio.get_event_loop()
        # self.setlayout()
        
        self.async_loop.run_until_complete(self.mainLoop(temp_pump_list, ratio, size))
   
        
        t.sleep(1)
       # self.spinMotor()
        t.sleep(1)
        #self.up()

        return True

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

        time = (ratio * int(size)) / 3
        print(time)
        print(pump)
       
        pump_list[pump-1].write(0)
        await asyncio.sleep(time)
        pump_list[pump-1].write(1)
    
    async def mainLoop(self, temp_pump_list, ratio, size):
        x=0
        pump = []
        stepper_motor_enable.write(0)
       
        '''
            ingredients:[
                'vodka': .10,
                'rum' : .20
            ]
        '''

        
        for a in temp_pump_list:
            pump.append(self.async_loop.create_task(self.findPump(a, ratio[a]['amount'], size)))
            x = x+1
        #pump.append(self.async_loop.create_task(self.down()))
        await asyncio.wait(pump)

  
class ratio(models.Model):
    menu_id= models.IntegerField()
    ingredient = models.CharField(max_length=50)
    amount = models.IntegerField()

    def create_drink(self, data):
        '''
            1) Grab the newly inserted Menu ID 
            2) For each new Item insert it into the data base

            ?) Profit?

            I will have to sync up with the front end on how we are going to build that object.
        '''


        new_entry = menu(id=last_id, name= data['name'], type_id=data['type'])
        new_entry.save()


        #1)
        menu_id = menu()
        #We should just be able to grab the last Id since we just inserted it, otherwise we gotta do some gay ass filering lol. 
        recent_id = menu_id.objects.values('id').last()
        

        ''' 
        Maybe how  this will look
            data = {
                "ingredients":[
                    rum,
                    whiskey,
                    coke,
                    drugs
                ],
                ratio:[
                    0.4,
                    0.4,
                    0.2
                ]
            }
        '''
        #2)
        for i in range(data['ingredients'].len())
            new_entry = ratio(menu_id = recent_id, ingredient = data['ingredients'][i], amount = data['ratio'][i])
            new_entry.save()




class progress(models.Model):
    in_progress = models.CharField(max_length=1)

    def check_progress(self):
        prog = progress.objects.all()       
        print(prog)
        if pump_components == 'n':
            return True
        else:
            return False
    
    def update_progress(self, x):
        prog = progress.objects.values('in_progress')
        prog['in_progress'] = x
        prog.save()




  