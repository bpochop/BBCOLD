from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.utils import serializer_helpers
from .serializers import RoomSerializer, CreateRoomSeriealizer #remove this
from .models import Room #Remove this

from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
# Create your views here.

class RoomView(generics.ListAPIView):
    #query set is what we want to return to the front end
    queryset = Room.objects.all()


    serializer_class = RoomSerializer


#lookups what settings we by checking the room number
#I dont think well need this. 
class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    #gets room number from the post request and grabs the arguement code so it can look it up
    #might be useful for grabbing post request for drink ingrediants
    def get(self,request, format = None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                #serializing the room and taking the data from the serializer
                data = RoomSerializer(room[0]).data
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Room Not FOund': "Invalid Room Code. "},status= status.HTTP_404)
        return Response({'Bad Request': 'Code Parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)

#Checking if room exists or maybe drink exists and shit
class JoinRoom(APIView):
    lookup_url_kwarg = 'code'
    def post(self, request, format=None):
        if not self.request.session.exits(self.request.session.session_key):
            self.request.session.create()
        
        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code = code)
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session['room_code'] = code
                return Response({'message': 'Room Joined!'}, status= status.HTTP_200_OK)
            
            return Response({'Bad Request': 'Invalid Room Code'}, status= status.HTTP_400_BAD_REQUEST)
    return Response({'Bad Request': 'Invalid post data, did not find a code key'}, status=status.HTTP_400_BAD_REQUEST)


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
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data, status = status.HTTP_202_ACCEPTED)
            else: 
                room = Room(host = host, guest_can_pause = guest_can_pause, votes_to_skip = votes_to_skip)
                room.save()
                self.request.session['room_code'] = room.code
            return Response(RoomSerializer(room).data, status = status.HTTP_201_CREATED)

class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exits(self.request.session.session_key):
            self.request.session.create()

        data = {
            'code': self.request.session.get('room_code')
        }
        return JsonResponse(data, status=status.HTTP_200_OK)
        
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