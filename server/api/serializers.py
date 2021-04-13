from django.db.models import fields
from rest_framework import serializers
from .models import menu, Ingredient_id, pumps, display, menu, ratio



class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = pumps
        fields = ('ingredient_id')
    
class PumpSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = pumps
        fields = ('pump', 'ingredient_id', 'volume_left')

class DisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = display
        fields = ('color', 'drinks_per_row')

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = menu
        fields = ('id', 'name', 'creator_id')

class RatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ratio
        fields = ('id', 'ingredient', 'amount')
#when your handling good idea to use a serializer, incoming or outgoing

