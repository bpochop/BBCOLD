from os import name
from django.db import models
import string
import random
import json
# Create your models here.
#PUT MOST OF YOUR LOGIC IN THE MODEL
#FATMODELS THIN VIEWS


nread = open("../../data/recipes.json", "r")
d = json.load(nread)
recipes = d["drinks"]
shotrecipies = d["shot"]
nread.close()




# def clean_pumps_list():

#     w = 1
#     y =1
#     temp = []


 
#     #here we are cleaning up the pumps list so we only get the alcohol, reason why we dont change this list in the json
#     #is because I think itll be easier to keep track of pins. Either way we have to remove the pumpx_y or add them
#     for x in pumps.values():
#         # print(x)
#         temp.append(x)
    

#     return temp



def generate_drink_Menu():

    menu = []
    count =0
    nread = open("../../data/pumps.json", "r")
    pumps = json.load(nread)
    nread.close()
    flag = False
    # print(recipes)

    #CHECKING IF THE COntents(fucking clown misspelled it) OF A DRINK ARE IN THE PUMPS LIST
    for x in recipes:

    """
    Recipes is built like this, its built DIFFERENT

    {
      "name": "Rum and Coke",
      "ingredients": {
        "Rum":0.25,
        "Coke":0.75
      },
      "img": "rumandcoke.png"
    },

    X should equal name, ingredients, img
    """

        #indicie of liquour list
      
        for y in x['ingredients']:

            """
                y should = ingrediants
                y = "Rum", Coke
                y.value() = .25, .75

            """
            if y in pumps.values():
                menu.append(y)


            print("DRINK NAME: " + y)
            print("DRINK RATIO: " + y.values())

            

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

class pumps(models.Model):
    #JUST PULL DATA FROM DATABASE ON WHATS IN THE PUMPS, WE NEED TO BE ABLE TO INSERT THEM INTO THE DATABASE, SO BUILD OUT ROUTING TO FRONT END.
    pump = models.CharField(max_length=50, unique=True)
    alcohol = models.CharField(max_length=50, unique=True)
    garnish = models.CharField(max_length=50, unique=True)
    other = models.CharField(max_length=50, unique=True)

class display(models.Model):
    #THIS IS FOR LATER FOR STYLING IF WE NEED THIS
    color = models.CharField(max_length=50, unique=True)
    drinks_per_row = models.IntegerField(max_length=50)
  

class menu(models.Model):
    #CLEAN THIS UP SOME, SEEMS MESSY. GOTTA COME UP WITH A DIFFERENT SCHEMA
    name = models.CharField(max_length=50, unique=True)
    alcohol = models.CharField(max_length=50)
    ratio = models.IntegerField()
   
        