from rest_framework import serializers
from .models import Room

#class below should match some fields in this class
class RoomSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Room
        fields= ('id', 'code', 'host', 'guest_can_pause', 'votes_to_skip','created_at')
        #automatically a id field in every model


#this class takes the post request and puts it into a python format
class CreateRoomSeriealizer(serializers.ModelSerializer):
    class Meta: 
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')





#when your handling good idea to use a serializer, incoming or outgoing

