from django.db.models import fields
from rest_framework import serializers
from .models import Room, menu, Ingredient_id, pumps, display, menu, ratio

#class below should match some fields in this class
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'code', 'host', 'guest_can_pause',
                  'votes_to_skip', 'created_at')

#this class takes the post request and puts it into a python format
class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')



class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient_id
        fields = ('ingredient_id', 'ingredient')

class PumpSerializer(serializers.ModelSerializer):
    class Meta:
        model = pumps
        fields = ('pump', 'ingredient_id')

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
        fields = ('id', 'ingredient_id', 'amount')
#when your handling good idea to use a serializer, incoming or outgoing

