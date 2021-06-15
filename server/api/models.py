from os import name, truncate
from django.db import models
import string
import random
import json
import time as t
import threading
import asyncio
import json
from datetime import datetime
#import pyfirmata

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
# board0 = pyfirmata.Arduino('/dev/ttyUSB0')
# ####Initializing arduino pin for the steppper motor inside main station
# stepper_motor_dir = board0.get_pin('d:2:o')
# stepper_motor_step = board0.get_pin('d:3:o')
# stepper_motor_enable = board0.get_pin('d:7:o')
# mixer_motor = board0.get_pin('d:4:o')

drink_in_progress = False

def write_logs(log, message):
    buff_time = datetime.now()
    current_time = buff_time.strftime("%H:%M:%S")
    log.write(current_time + "   " + message +  "\n")

# mixer_motor.write(1)
# stepper_motor_enable.write(1)

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
    db_size = pumps.objects.count()
    actual_pumps = len(pump_list)\
    
    print(db_size)

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

    width = "400"
    height="500"
   
    ingredient= models.CharField(primary_key = True,max_length=50, unique=True)
    dtype = models.CharField(max_length=2, unique = False, default= "a")
    pump_picture = models.ImageField(upload_to = "../../img", default = "../../img/default.png", height_field=None, width_field=None)

    def get_liquor(self):
        alc_list = []
        alc_list = Ingredient_id.objects.values('ingredient','pump_picture').filter(dtype="a")
        return alc_list
    
    def get_mixer(self):
        mixer_list = Ingredient_id.objects.values('ingredient', 'pump_picture').filter(dtype="m")
        return mixer_list

    def add_to_list(self, ingredient, dtype):
       
        Ingredient_id.objects.create(ingredient=ingredient, dtype = dtype)
        return True
    
    


        

class pumps(models.Model):
    
    #JUST PULL DATA FROM DATABASE ON WHATS IN THE PUMPS, WE NEED TO BE ABLE TO INSERT THEM INTO THE DATABASE, SO BUILD OUT ROUTING TO FRONT END.
    pump = models.IntegerField(primary_key = True, unique=True)
    ingredient_id = models.CharField(max_length = 100)
    volume_left = models.IntegerField()



    def get_pumps(self, log):
        write_logs(log,"We are in $BBC_HOME/server/api/models.py function get_pumps")
        pump_components = pumps.objects.values('pump','ingredient_id')
        return pump_components
    
    def update_pumps(self, data, log): 
        write_logs(log,"We are in $BBC_HOME/server/api/models.py function update_pumps ")
        string = ''
        #we may have to format the request object holding the pump data, it depends how the front end sends it. 

        for x in data['pump_list']:
            print(x)
            pump_components = pumps.objects.get(pump = (x['pump']))
            pump_components.ingredient_id = x['ingredient']
            pump_components.save()
            string += "Pump: " + str(x['pump']) + " Ingredient: " + x['ingredient']
         
        
        write_logs(log,string)
       

       

    def get_pump_count(self):
        pump_components = pumps.objects.all().count()
        return (pump_components)
    
    def start_pump_prime(self, pump):
        pump_list[pump].write(1)
    
    def stop_pump_prime(self, pump):
        pump_list[pump].write(0)

        
    


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
        print(data)

        for x in data:
            name_array = {
                "name": "",
                "drink_id":"",
                "creator_id": "",
                "type_id": "",
                "ingredients":{},
                "picture": ""
            }
            name = menu.objects.values('name','creator_id', 'type_id', 'picture').filter(id=x)
            temp = ratio.objects.values('ingredient','amount').filter(menu_id=x)
            print(temp)
            
            type_id = name[0]['type_id']

            name_array['name'] = name[0]['name']
            name_array['creator_id'] = name[0]['creator_id']
            name_array['type_id'] = name[0]['type_id']


            name_array['ingredients']= temp
            name_array['picture'] = name[0]['picture']
            
            if type_id == "C":
                menu_data["C"].append(name_array)
            elif type_id == "S":
                menu_data["S"].append(name_array)
            elif type_id == "CS":
                menu_data["CS"].append(name_array)
        #print(menu_data)
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
    
    def create_drink(self, data,log):
        '''
            1) Grab last id inserted into database
            2) Increase Id
            3) create new Object for table
            4) Save


            
        '''
        write_logs(log,"We are in $BBC_HOME/server/api/models.py Model=Menu Function=create_drink")

        last_id = (menu.objects.values('id').last())
        last_id = int(last_id['id']) + 1
        new_entry = menu(id=last_id, name= data['name'], type_id=data['type'])
        write_logs(log, "Name = " + data['name'] + "\nType id =  " + data['type'] )
        try:
            new_entry.save()
        except:
            return(False)





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
                3) GRAB ALL INFORMATION WE NEED FOR CALCULATIONS
                4) GRAB ALL ITEMS WE NEED TO INCRESE/DECRESE FOR SLIDER
                5) RUN A CHECK TO SEE IF WE CAN EVEN INCREASE VALUES AS WE HAVE SOME RECIPES THAT CONTAIN ALL LIQUOR
                6) RATIO MATH
                7) FIND PUMPS WE NEED TO EXECUTE ON
                8) SEND INFO TO BE ADDED TO OUR TASK LIST
                9) EXECUTE IT ASYNCHRONOUSLY (FUUUUUUUCCKKKKK)
                
                EXTRA CREDIT ;):
                    1) GET THEM LED'S FOOKIN WORKING AMRIGHT


            OLD CODE
                1) WE THREADED THE PUMPS DUE TO THE GUI NOT WORKING WHILE THE PUMPS RAN. WE MAY NOT NEED TO DO THAT SINCE WE ARE RUNNING A WEBSERVER (def createloadingwindow)
                2) WE THEN WENT TO A BUFFER FUNTION, THIS FUNCTION ADDED OUR TASK (DISPENSING PUMPS) TO THE LIST/ARRAY OF WORK WE NEEDED TO GET DONE. EACH PUMP THAT WE NEEDED GOT ADDED TO THE LIST. 
                3) WE THEN BEGAN THE WORK OF FIND OUT WHICH PUMP HAD WHICH INGREDIENT AND THEN TELLING THAT PUMP TO TURN ON. 
        '''
       
        #1. BAEFY SECURED, MOVING OUT

        #2. GRAB ALL THE PUMP INGREDIENTS
        pump_components2 = pumps.objects.values('pump','ingredient_id')
    
   
        #3) GRAB ALL INFORMATION WE NEED FOR CALCULATIONS
        '''
            HOPEFULLY WE CAN CREATE THE DATA SO ITS INTHE FORMAT OF 
            REQUEST:[
                'menu_id': "ARKANSAS RAZERBACK,
                'size' : 'M',
                'ratio: .21
            ]

        '''

        menuid = menu.objects.values('id').filter(name=request['menu_id'])

        
        recipe_id = ratio.objects.filter(menu_id = menuid[0]['id'])
       
        size = request['size']
        adjust_ratio = request['ratio']
        liquor_list = Ingredient_id.objects.filter(dtype = "a")
        lcount = []
        clean_list = []
        mcount = []
        final_list = []
        ltotal = 0
        mtotal =0


       
        for x in liquor_list:
            clean_list.append(x.ingredient)

      


        #4) GRAB ALL ITEMS WE NEED TO INCRESE/DECRESE FOR SLIDER
        for x in recipe_id:
            drink_obj = {
                "ingredient": '',
                "amount": 0,
                'pump': 0
            }
            if x.ingredient in clean_list:
                drink_obj['ingredient'] = x.ingredient
                drink_obj['amount'] = x.amount
                ltotal = ltotal + x.amount
                lcount.append(drink_obj)
            else:
                drink_obj['ingredient'] = x.ingredient
                drink_obj['amount'] = x.amount
                mtotal = mtotal + x.amount
                mcount.append(drink_obj)

        alcohol_ratio = ltotal / (mtotal + ltotal)
    
      
        # 5) RUN A CHECK TO SEE IF WE CAN EVEN INCREASE VALUES AS WE HAVE SOME RECIPES THAT CONTAIN ALL LIQUOR
        if len(lcount) == len(recipe_id):
            final_list = lcount
            
            #skip Ratio math
        else: 

            '''
                WE MAY NEED TO TUNE THIS
                THE GREAT RATIO ADJUSTER:
                1)    1% - 20% ALCOHOL = MAX_RATIO OF 40%
                2)    21% - 40% ALCOHOL = MAX_RATIO OF 25%
                3)    40% - 60% ALCOHOL = MAX_RATIO OF 15%
                4)    60% - 100% ALCOHOL = MAX_RATIO OF 10% 

                    check what amount they put and see if it falls within our matrix ratio

            '''
            # print("Alcohol Ratio: ", alcohol_ratio)

            # print("Adjusted Ratio: ", int(adjust_ratio)/100)
            adjust_ratio = int(adjust_ratio)/100


            if adjust_ratio == 0:
                print("0")
                final_list = self.calculate_ratios(lcount,mcount, adjust_ratio)
            elif (alcohol_ratio >.1 and alcohol_ratio <= .20 ) and adjust_ratio > .40:
                adjust_ratio = .40
                print("1")
                final_list = self.calculate_ratios(lcount,mcount, adjust_ratio)
            elif (alcohol_ratio > .21 and alcohol_ratio <=.40) and adjust_ratio > .25:
                adjust_ratio = .25
                print("2")
                final_list = self.calculate_ratios(lcount,mcount, adjust_ratio)
            elif (alcohol_ratio > .41 and alcohol_ratio <= .60) and adjust_ratio > .15:
                adjust_ratio = .15
                print("3")
                final_list = self.calculate_ratios(lcount,mcount, adjust_ratio)
            elif (alcohol_ratio >= .61) and adjust_ratio > .10:
                adjust_ratio = .10
                print("4")
                final_list = self.calculate_ratios(lcount,mcount, adjust_ratio)
            else:
                print("nothing lmao")
                final_list = self.calculate_ratios(lcount,mcount, adjust_ratio)
            


        # 7) FIND PUMPS WE NEED TO EXECUTE ON
        clean_list = []
        for x in pump_components2:
            clean_list.append(x['ingredient_id'])

        for x in final_list:
            for y in pump_components2:
                if x['ingredient'] == y['ingredient_id']:
                    x['pump'] = y['pump']

        #7.5) Format size
        '''
         size =    small = 90 militers
             size =    medium = 150 militers
             size =    large = 210 militers
              size =   shot = 40 milter
        '''
        if size == "small":
            size = 90
        elif size == "medium":
            size = 150
        elif size == "large":
            size =210
        elif size == "shot":
            size = 40
            

        print(final_list)
        # 8) SEND INFO TO BE ADDED TO OUR TASK LIST    
        self.buffer_function(final_list,size)
        return True

    def calculate_ratios(self, llist, mlist, ratio):
          
        # 6) RATIO MATH
            '''
               P = percentage we want to increase/decrease by
               1 = 1 complete drink
               N = new complete drink after we subtract the increased ratio. 

               ex. 

               we want to increase the drink by 32%

               alcohol 1 = .30
               alcohol 2 = .40
               mixer 3 = .20
               mixer 4 = .10
              
                #1 (.30 + .40) = .70
               

                #2
                alcohol ratio (alcohol * % you want to raise by) = .70 * 1.32% = .924
                alcohol ratio = .924

                #3
                alcohol 1 = (.40/.70) * .924 = .528
                alcohol 2 = (.30/.70) * .924 = .396

                #4
                mixer ratio = 1 - .924 = .076
                the new total can't be 100, it has to be whatever is left that needs to be decreased soooooooo

                #5
                .20 + .10 = .30

                #6
                mixer 3 = (.20/.30) * .076 = .05066666
                mixer 4 = (.10/.30) * .076 = .025333333

                    

                final mixed drink ratio =  .396 + .3451 + .17257 + .08628 = .999999995 (we lost some precision with a normal calculator but the computer wont loose precision hehee)


                #7
                merge lists 

            '''
            finalList = []

            if ratio == 0:
                #merge lists
                pass
            else: 
                a_total = 0
                #1 grabbing total amount of liquor in drink
                for x in llist:
                    a_total = a_total + x['amount']

                #2
                a_ratio = a_total * (1 + ratio)

                #3
                count=0
                for x in llist:
                    llist[count]['amount'] = (x['amount']/a_total) * a_ratio
                    count+=1
                
                #4
                m_ratio = 1 - a_ratio

                #5
                m_total = 0
                for x in mlist:
                    m_total = m_total + x['amount']
                
                #6
                count = 0
                for x in mlist: 
                    mlist[count]['amount'] = (x['amount']/m_total) * m_ratio
                    count += 1
            


            #DOING THIS BECAUSE IT GAVE ME A WEIRD NESTED ARRAY WHEN IT DIDNT NEED TO BE. 
            for x in llist:
                finalList.append(x)

            for x in mlist:
                finalList.append(x)

          

            return finalList

                



        
    
    def buffer_function(self, drink_list, size):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.async_loop = asyncio.get_event_loop()
        # self.setlayout()
        
        self.async_loop.run_until_complete(self.mainLoop(drink_list, size))
   
        
        t.sleep(1)
       # self.spinMotor()
        t.sleep(1)
        #self.up()

        return True

    async def mainLoop(self, drink_list, size):
        x=0
        pump = []
        #stepper_motor_enable.write(0)
       
        for a in drink_list:
            pump.append(self.async_loop.create_task(self.findPump(a['pump'], a['amount'], size)))
            x = x+1
        #pump.append(self.async_loop.create_task(self.down()))
        await asyncio.wait(pump)

      
      

    async def findPump(self, pump, ratio, size):
          #5) CALCULATE HOW LONG THE PUMPS NEED TO RUN BASED ON SIZE OF CUP
        '''
            DATA WE ARE WORKING WITH:
             size =    small = 90 militers
             size =    medium = 150 militers
             size =    large = 210 militers
              size =   shot = 40 milters
                
                ratio = .3 out of 1 or 1/3
            
            formula: time = (ratio * size) / 3
            3 militers per second maybe?

            I cant remember why we are diving by 3 but well figure it out when we test LOL
        '''
        


        time = (ratio * int(size)) / 3
        print(time)
        print(pump)
       
        # pump_list[pump-1].write(0)
        await asyncio.sleep(time)
        # pump_list[pump-1].write(1)
    

        

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

   
  
class ratio(models.Model):
    menu_id= models.IntegerField()
    ingredient = models.CharField(max_length=50)
    amount = models.CharField(max_length = 4)

    def create_drink(self, data, log):
        '''
            1) Grab the newly inserted Menu ID 
            2) For each new Item insert it into the data base

            ?) Profit?

            I will have to sync up with the front end on how we are going to build that object.
        '''

        #1)
        menu_id = menu()
        #We should just be able to grab the last Id since we just inserted it, otherwise we gotta do some dumb ass filering lol. 
        recent_id = menu.objects.values('id').last()
        

        ''' 
            "ingredients":{
                    rum,
                    whiskey,
                    coke,
                    drugs
                },
                ratio:{
                    0.4,
                    0.4,
                    0.2,
                    0.2
                }
            }
        '''
        #2)
        log_string = ""
        for i in data['ingredients']:
           new_entry = ratio(menu_id = int(recent_id['id']), ingredient = i, amount = data['ingredients'][i])
           new_entry.save()
           log_string += "\nId: " + str(recent_id['id']) + "\nIngredient: " + i + "\nRatio: " + str(data['ingredients'][i])

        write_logs(log, log_string)




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




  