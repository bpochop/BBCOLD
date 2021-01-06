from os import name
from django.db import models
import string
import random
import json
# Create your models here.
#PUT MOST OF YOUR LOGIC IN THE MODEL
#FATMODELS THIN VIEWS


# nread = open("../../data/recipes.json", "r")
# d = json.load(nread)
# recipes = d["drinks"]
# shotrecipies = d["shot"]
# nread.close()

# nread = open("../../data/pumps.json", "r")
# pumps = json.load(nread)
# nread.close()


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



# def generate_drink_Menu():

#     menu = []
#     count =0
#     p = clean_pumps_list()
#     flag = False
#     # print(recipes)

#     #CHECKING IF THE CONENTS OF A DRINK ARE IN THE PUMPS LIST
#     for x in recipes:

#         #indicie of liquour list
#         count = count +1
    
#         for y in x['content']:

#             if x['content'][y] in p:
#                 flag = True
#             elif isinstance(x['ratio'][y + "r"], str):
#                 flag = True
#             else:
#                 flag = False
#                 break
        
#         if flag is True:
#             menu.append(x)


#     for x in menu:
#         print(x["name"])


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

class menu(models.Model):
    name = models.CharField(max_length=50, unique=True)
    i1 = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i2 = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i3= models.CharField(max_length=50, null = True, blank=True, unique=True)
    i4 = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i5 = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i6 = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i7 = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i8 = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i9 = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i10 = models.CharField(max_length=50, null = True, blank=True, unique=True)
    
    i1r = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i2r = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i3r = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i4r = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i5r = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i6r = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i7r = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i8r = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i9r = models.CharField(max_length=50, null = True, blank=True, unique=True)
    i10r = models.CharField(max_length=50, null = True, blank=True, unique=True)

    img = models.ImageField()