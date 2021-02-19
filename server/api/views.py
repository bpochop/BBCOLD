from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.utils import serializer_helpers
from .serializers import RoomSerializer, CreateRoomSerializer, PumpSerializer, IngredientSerializer, RatioSerializer 
from .models import Room, pumps, ratio, menu
import json, collections

from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
# Create your views here.

class RoomView(generics.ListAPIView):
    #query set is what we want to return to the front end
    queryset = Room.objects.all()




class pumpsView(APIView):
  
    # def get(self, request, format = None):

    #     print("were in get")

    #     if request.method == "POST":
    #         set_pumps(request)
    #     else:
    #         get_pumps(request)
          

    def fetch(self, request, format = None):
        print("were in get_pumps")
        pump_components = pumps.objects.all()
        #print(pump_components)
        pump_data = PumpSerializer(pump_components, many=True)

        y=0
        for x in pump_data.data:
            y = y+1

        print(y)
        testObject = {
            'message': 'getfucked pussy'
        }


        return_obj = {
            "total": y,
            "pumps":pump_data.data
        }
      
        
        return Response(return_obj, status= status.HTTP_200_OK, content_type="application/json")

    def post(self, request):
        # pump_components = pumps.objects.get()
        # #change pump_obj to whatever edrian sends to the backend. 
        # change = request.GET.get('pump_obj')

        print(request.GET.get('pump_obj'))



class menuView(APIView):
    '''
        HELPER FUNCTIONS

    '''
    def buildObject(self, data):
        #3)Graab name of all recipies that make it through the filter
        #4) Build an object to send to the front end. 

        print(data)
        idx =0
        menu_data = {
            "C":[
            ],
            "S":[],
            "CS":[

            ]
        }


        for x in data:
        
            name_array = {
                "name": "",
                "creator_id": "",
                "type_id": "",
                "ingredients":{}
            }
            name = menu.objects.values('name','creator_id', 'type_id').filter(id=x)
            temp = ratio.objects.values('ingredient','amount').filter(menu_id=x)
            
       
            type_id = name[0]['type_id']

            name_array['name'] = name[0]['name']
            name_array['creator_id'] = name[0]['creator_id']
            name_array['type_id'] = name[0]['type_id']
            name_array['ingredients']  = temp[0]
            
            if type_id == "C":
                menu_data["C"].append(name_array)
            elif type_id == "S":
                menu_data["S"].append(name_array)
            elif type_id == "CS":
                menu_data["CS"].append(name_array)

        return menu_data
            
            

    
    def get(self, request, format = None):
        """
            Goal
                1) Grab all menu items that have ingredients in common with the pump list
                2) Filter out any Recipies that dont contain all the ingredients in the pump list
                    ex 
                        Rum and Coke [Rum,Coke]
                        Pumps [Vodka, Rum]
                        filter out Rum and Coke because it contains Coke
                3)Graab name of all recipies that make it through the filter
                4) Build an object to send to the front end. 
        """
        pump_components = pumps.objects.values('ingredient_id')
        pump_list = []
        #pump_data = IngredientSerializer(pump_components)
        data = []

        ingredients_list = {}
        
        size =0

        grab = []
        #1) Grab all menu items that have ingredients in common with the pump list
        for x in pump_components:
            #print(x['ingredient_id'])
            #FIRST GRAB ALL MENU_ID'S THAT HAS THAT INGREDIENT IN COMMON WITH X
            if x['ingredient_id'] != '' :
                pump_list.append(x['ingredient_id'])
                
                temp = (ratio.objects.values('menu_id').filter(ingredient=x['ingredient_id']))
                #GRABBING ALL RECIPE ID'S THAT HAVE A INGREDIENT IN COMMON WITH PUMP LIST
                for y in temp:
                    if y['menu_id'] not in grab:
                        grab.append(y['menu_id'])

        

        #now I have all the menu ID's that contain the ingredients in the ingredients list
        bad_list = []


        #2) Filter out any Recipies that dont contain all the ingredients in the pump list
        for x in grab: 
            temp = ratio.objects.values('ingredient','amount').filter(menu_id=x)
            for y in temp: 
                print(y)
                if type(y['amount']) is float or type(y['amount']) is int:
                    if y['ingredient'] not in pump_list:
                        if x not in bad_list:
                            bad_list.append(x)
                
        #getting the difference of the 2 lists to grab all the good data. 
        diff_list1_list2 = set(bad_list) - set(grab)
        diff_list2_list1 = set(grab) - set(bad_list)
        data = list(diff_list1_list2) + list(diff_list2_list1)

        print(data)

        menu_data = self.buildObject(data)
        
        return Response(menu_data, status= status.HTTP_200_OK, content_type="application/json")

    
    def confirm(self, request, format = None ):
        '''
            HERE IS WHERE WE WILL EXECUTE THE PUMP CODE.
            GOALS:
                1) GET A BAEFY
                2) GRAB ALL PUMP INGREDIENTS
                3) GRAB FROM THE FRONT END THE INGREDIENTS AND AMOUNT
                4) FIND WHAT PUMP IS WHAT AND EXECUTE IT ASYNCHRONOUSLY (FUUUUUUUCCKKKKK)
                
                EXTRA CREDIT ;):
                    1) GET THEM LED'S FOOKIN WORKING AMRIGHT
        '''

        return Response("WHATS COOKIN, GOOD LOOKIN ;)", status= status.HTTP_200_OK, content_type="application/json")





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


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer



    def post(self, request, format=None):
        #if current user has an active session with our website, I dont think well need this for our program 
        if not self.request.session.exists(self.request.session.session_key):
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
        if not self.request.session.exists(self.request.session.session_key):
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

# def confirm(request):
#     return HttpResponse("Confirm")