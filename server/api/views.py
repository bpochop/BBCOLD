from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.utils import serializer_helpers
from .serializers import PumpSerializer, IngredientSerializer, RatioSerializer 
from .models import pumps, ratio, menu, settings, check_config, get_stations, progress, Ingredient_id
import json, collections

from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
# Create your views here.

check_config()
confirm_class = settings()


class pumpsView(APIView):

    def get(self, request, format = None):
        return_obj = []
        newpumps = pumps()
        return_obj = newpumps.get_pumps()
        return Response(return_obj, status= status.HTTP_200_OK, content_type="application/json")

class UpdatePumps(APIView):

    def post(self, request, format= None):
        pumpclass = pumps()
        pumpclass.update_pumps(request)
        return_obj = pumpclass.get_pumps()
        return Response({'message': 'Pumps'}, status = status.HTTP_200_OK, content_type = "application/json")


class CreateDrink(APIView):

    def post(self, request, format = None):       

        menu_class = menu()
        menu_class.create_drink(request.data)


        ratio_class = ratio()
        ratio_class.create_drink(request.data)

        menu_class.create_drink()

class SettingsView(APIView):

    def post(self, request,format=None):
        settings_mode = settings()
        count=""

        if (request.data['data']  == "Motor_up"):
            settings_mode.mixer_up()
            count="Motor is up"

        elif(request.data['data']  == "Motor_down"):
            settings_mode.mixer_down()
            count="Motor is down"
        elif(request.data['data']  == "clean_pump"):
            settings_mode.clean_pump()
            count="cleaning"
        elif(request.data['data']  == "get_stations_count"):
            pump_class = pumps()
            count = pump_class.get_pump_count()
        elif(request.data['data'] == "start_prime_stations"):
            pump_class = pumps()
            pump_class.start_pump_prime(request.data['pump'])
            count="stop priming"
        elif(request.data['data'] == "stop_prime_stations"):
            pump_class = pumps()
            pump_class.start_pump_prime(request.data['pump'])
            count="stop priming"
        elif(request.data['data'] == "update_pump"):
            pump_class = pumps()
            pump_class.update_pumps(request.data['pump_list'])
            count = "updated"
        elif(request.data['data'] == "add_station"):
            settings_mode.detect_Pumps
            count="Adding Station"
        
        return Response(count, status=status.HTTP_200_OK,  content_type="application/json")
        



class menuView(APIView):
  
    def post(self,request,format=None):

        menu_data = []
     
        if request.data['data'] == "filtered_menu":
            menu_class = menu()
            menu_data = menu_class.get_menu()
        elif request.data['data'] == "get_liquor":
            ingredient_list = Ingredient_id()
            print("is it getting here?")
            menu_data = ingredient_list.get_liquor()
        elif request.data['data'] == "get_mixer":
            ingredient_list = Ingredient_id()
            print("is it getting here?")
            menu_data = ingredient_list.get_mixer()
        elif request.data['data'] == "add_to_list":
            ingredient_list = Ingredient_id()
            ingredient_list.add_to_list(request.data['item'], request.data['type'])

            
        
        return Response(menu_data, status= status.HTTP_200_OK, content_type="application/json")

    

class confirmView(APIView):

    def post(self,request, format=None):
        #new plan store a value in the database to see if a session is already running. 

        # prog = progress()
        # print(prog.check_progress)
        print(request.data)
        
        #check_config()
        confirm_class = settings()
        confirm_class.confirm(request.data)
 
        #confirm_class.mixer_up()

        return Response("making drink", status= status.HTTP_200_OK, content_type="application/json")


#Checking if room exists or maybe drink exists and shit
class JoinRoom(APIView):
    lookup_url_kwarg = 'code'
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
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


# class CreateRoomView(APIView):
#     serializer_class = CreateRoomSerializer


#     def post(self, request, format=None):
#         #if current user has an active session with our website, I dont think well need this for our program 
#         if not self.request.session.exists(self.request.session.session_key):
#             self.request.session.create()

#         #take our data and give us a python version, WE WILL NEED THIS BABY
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             guest_can_pause = serializer.data.get('guest_can_pause')
#             votes_to_skip = serializer.data.get('votes_to_skip')
#             host = self.request.session.session_key
#             #checking our database to see if a host has an active session already, may need this?
#             queryset = Room.objects.filter(host =host)
#             if queryset.exists():
#                 room = queryset[0]
#                 room.guest_can_pause = guest_can_pause
#                 room.votes_to_skip = votes_to_skip
#                 room.save(update_fields = ['guest_can_pause', 'votes_to_skip'])
#                 self.request.session['room_code'] = room.code
#                 return Response(RoomSerializer(room).data, status = status.HTTP_202_ACCEPTED)
#             else: 
#                 room = Room(host = host, guest_can_pause = guest_can_pause, votes_to_skip = votes_to_skip)
#                 room.save()
#                 self.request.session['room_code'] = room.code
#             return Response(RoomSerializer(room).data, status = status.HTTP_201_CREATED)

        
#Method 2

# def create(request):
#     return HttpResponse("Create")

# def settings(request):
#     return HttpResponse("Settings")

# def maintenance(request):
#     return HttpResponse("Maintenance")
