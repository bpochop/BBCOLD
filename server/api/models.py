from os import name, truncate
from django.db import models
import string
import random
import json
# Create your models here.
#PUT MOST OF YOUR LOGIC IN THE MODEL
#FATMODELS THIN VIEWS


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

    # fill = [
    #     (" ", " "),
    #     ("Vodka", 'Vokda'),
    #     ("Citrus Vodka", "Citrus Vodka"),
    #     ("Whiskey", "Whiskey"),
    #     ("Crown-Royal Apple", "Crown-Royal Apple"),
    #     ("Crown-Royal Vanilla", "Crown-Royal Vanilla"),
    #     ("Rum", "Rum"),
    #     ("Bourbon","Bourbon"),
    #     ("Tequila", "Tequila"),
    #     ("Jagermeister", "Jagermeister"),
    #     ("Hennessy","Hennessy"),
    #     ("Midori", "Midori"),
    #     ("Gin", "Gin"),
    #     ("Brandy", "Brandy"),
    #     ("Absinthe","Absinthe"),
    #     ("Moonshine","Moonshine"),
    #     ("Everclear", "Everclear"),
    #     ("Sake","Sake"),
    #     ("Soju", "Soju"),
    #     ("Kahlua", "Kahlua"),
    #     ("Baileys", "Baileys"),
    #     ("Sweet Vermouth","Sweet Vermouth"),
    #     ("Campari", "Campari"),
    #     ("White Rum", "White Rum"),
    #     ("Vodka Citron",
    #     "Blue Curacao",
    #     "Amaretto",
    #     "Wine",
    #     "Triple Sec",
    #     "Rye",
    #     "Schnapps",
    #     "Peach Schnapps",
    #     "Cognac",
    #     "Brandy",
    #     "Chambord",
    #     "Creme de Violette",
    #     "Vermouth",
    #     "Banana Liquer",
    #     "Lychee Liqueur",
    #     "Grenadine",
    #     "Orange Juice",
    #     "Simple Syrup",
    #     "Pineapple Juice",
    #     "Apple Juice",
    #     "Lime Juice",
    #     "Lemon Juice",
    #     "Blueberry Lemonade",
    #     "Lemonade",
    #     "Sprite",
    #     "Coke",
    #     "Orange Soda",
    #     "Squirt",
    #     "Ginger Beer",
    #     "Cranberry Juice",
    #     "Sour Mix",
    #     "Limeade",
    #     "Water",
    #     "Mint",
    #     "Kool-aid",
    #     "Apple Cider",
    #     "Sweet Tea",
    #     "Ginger Ale",
    #     "Orgeat Syrup",
    #     "Limeade",
    #     "Angostura bitters",
    #     "Orange bitters",
    #     "Peychauds Bitters",
    #     "Cherry",
    #     "Lime Slice",
    #     "Orange Slice",
    #     "Lemon Slice",
    #     "Mint leaves",
    #     "Sugar Cube",
    #     "Raspberries",
    #     "Ice"
    # ]
    ingredient_id = models.IntegerField(primary_key=True, unique= True)
    ingredient= models.CharField(max_length=50, unique=True)

class pumps(models.Model):
    
    #JUST PULL DATA FROM DATABASE ON WHATS IN THE PUMPS, WE NEED TO BE ABLE TO INSERT THEM INTO THE DATABASE, SO BUILD OUT ROUTING TO FRONT END.
    pump = models.IntegerField(primary_key = True, unique=True)
    ingredient_id = models.CharField(max_length = 100)
    volume_left = models.IntegerField()



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

    id = models.IntegerField(primary_key =True, unique=True)
    name = models.CharField(max_length=50, unique=True)
    creator_id = models.CharField(max_length=20, default="BBC")
    type_id = models.CharField(max_length=2)
   
  
class ratio(models.Model):
    menu_id= models.IntegerField()
    ingredient = models.CharField(max_length=50)
    amount = models.IntegerField()