from rest_framework import serializers
from .models import Room, menu

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


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = menu
        fields = ('name', 'i1', 'i2', 'i3',
                  'i4', 'i5', 'i6', 'i7', 'i8', 
                  'i9', 'i10','i1r', 'i2r', 'i3r', 
                  'i4r', 'i5r', 'i6r', 'i7r', 'i8r', 
                  'i9r', 'i10r', 'img' )

#when your handling good idea to use a serializer, incoming or outgoing

