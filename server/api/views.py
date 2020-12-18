from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.utils import serializer_helpers
from .serializers import RoomSerializer, CreateRoomSeriealizer #remove this
from .models import Room #Remove this

from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.

class RoomView(generics.ListAPIView):
    #query set is what we want to return to the front end
    queryset = Room.objects.all()


    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    serializer_class = CreateRoomSeriealizer



    def post(self, request, format=None):
        #if current user has an active session with our website, I dont think well need this for our program 
        if not self.request.session.exits(self.request.session.session_key):
            self.request.session.create()

        #take our data and give us a python version, WE WILL NEED THIS BABY
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            #checking our database to see if a host has an active session already, may need this?
            queryset = Room.objects.filter(host =host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields = ['guest_can_pause', 'votes_to_skip'])
                return Response(RoomSerializer(room).data, status = status.HTTP_202_ACCEPTED)
            else: 
                room = Room(host = host, guest_can_pause = guest_can_pause, votes_to_skip = votes_to_skip)
                room.save()

            return Response(RoomSerializer(room).data, status = status.HTTP_201_CREATED)


#Method 2
# def home(request):
#     return HttpResponse("hello test my guy")

# def create(request):
#     return HttpResponse("Create")

# def settings(request):
#     return HttpResponse("Settings")

# def maintenance(request):
#     return HttpResponse("Maintenance")

# def menu(request):
#     return HttpResponse("Menu")

# def confirm(request):
#     return HttpResponse("Confirm")