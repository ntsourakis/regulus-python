from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from .models import State
from ast import literal_eval
import json
import uuid
import sys
#sys.path.append('./dante/python/')
#sys.path.append('/app/poetry/python/')
import dante.python.lite_call_runtime_top as call
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

States = {};

def DantePageView(request):
    return HttpResponse('Hello, Dante!')

	
class DanteInitView(APIView):
    permission_classes = (IsAuthenticated,)
			
    def get(self, request): 

        model = State
        
        #l_newState = call.init_basic()
        
        l_stateId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        #l_stateId = uuid.uuid4().hex # generate unique Id for state
        
        ##State.objects.create(userId=request.META.get('HTTP_AUTHORIZATION').split(' ')[1], current=l_newState)
        ##State.objects.userId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        ##State.objects.current = l_newState
        ##State.objects.save()
		
        #state, created = State.objects.get_or_create(userId=request.META.get('HTTP_AUTHORIZATION').split(' ')[1], current=l_newState)

        #if created:
        #    print ("--- INIT | New user: %s #" % l_stateId)
        #else:
        #    print ("--- INIT | Existing user: %s #" % l_stateId)
   
        try:
            currentState = State.objects.get(userId=l_stateId)
        except State.DoesNotExist:
            currentState = None
        
        if currentState:
            print("--- INIT | Existing user: %s #" % l_stateId)           
            l_result = {'stateId':l_stateId, 'state':currentState.__str__()}
        else:
            print("--- INIT | New user: %s #" % l_stateId)
            l_newState = call.init_basic()
            print("--- INIT | type(l_newState): %s #" % type(l_newState))	
            State.objects.create(userId=l_stateId, current=l_newState)
            l_result = {'stateId':l_stateId, 'state':l_newState}
			
		##model.(l_newState)
		
		##setattr(f, l_newState)
		##f.save()

        ##l_newState = call.init_state('C:/Projects/django/callector/api/python/call_tables.data.gz', 'C:/Projects/django/callector/api/python/robust_matching_tables.data.gz')
        ##l_newState = call.init_state('C:/Projects/django/callector/api/lite_call_python/call_tables.data.gz', 'C:/Projects/django/callector/api/lite_call_python/robust_matching_tables.data.gz')
        
        #States[l_stateId] = l_newState
        #TODO
        #print (">>>>>>> INIT >>>>>>> States[l_stateId] : %s" % States[l_stateId])
        #print (">>>>>>> INIT >>>>>>> States : %s" % States)
		
		##request.session['l_stateId'] = l_newState
        ##fav_color = request.session.get('fav_color')
        ##print(fav_color)
        ##request.session['fav_color'] = 'blue'
        ##fav_color = request.session.get('fav_color')
        ##print(fav_color)
        ##for key, value in request.session.items():
        ##    print('{} => {}'.format(key, value))
        #l_result = {'stateId':l_stateId, 'state':l_newState}
        
        ##if 'fav_color' in request.session:
        ##   print(request.session['fav_color'])
        ##request.session['fav_color'] = 'blue'        
        
        return Response(l_result)
    
class DanteMessageView(APIView):
    permission_classes = (IsAuthenticated,)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
			
    def post(self, request):

        model = State
		
        req = json.loads(request.body)
        l_stateId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        #l_stateId = req['state']
        l_message = req['message']
        #print (">>>>>>> MESSAGE >>>>>>> l_message : %s" % l_message)
        print("l_stateId:")
        print(l_stateId)
        #print("l_state")
        #l_state = request.session['l_stateId']

        ##for key, value in request.session.items():
        ##    print('{} => {}'.format(key, value))
        ##fav_color = request.session.get('fav_color')
        ##print(fav_color)
        ##print ("len(States) : %d" % len (States))
        ##print (">>>>>>> MESSAGE >>>>>>> States : %s" % States)
        
		#l_state = States[l_stateId]
        try:
            l_state = State.objects.get(userId=l_stateId)
        except State.DoesNotExist:
            l_state = None
        
        print("--- MESSAGE | Current state: %s #" % l_state)
        ##st = request.session['States']
        
        ##print ("len(States) : %d" % len (States))
		##print(l_state);
        ##if 'fav_color' in request.session:
        ##   print(request.session['fav_color'])
		
        ##l_state=State.objects.get()
        ##print("l_state")
        ##print ("l_state : %s" % l_state)
        print("--------------------")
        #print(json.loads(l_state.__str__()))
        python_dict = literal_eval(l_state.__str__())
        print("--- MESSAGE | type(python_dict): %s #" % type(python_dict))	
        print(python_dict)
        l_result = call.message_and_state_to_message(l_message, python_dict)
        print("--- Message | New state: %s #" % python_dict)
        ##print ("l_result : %s" % l_result)
        ##print ("l_state : %s" % l_state)
        #States[l_stateId] = l_state
        State.objects.filter(userId=l_stateId).update(current=python_dict)
        ##print (">>>>>>> MESSAGE >>>>>>> States[l_stateId] : %s" % States[l_stateId])
        
        return Response(l_result)

class DanteRobustView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        
        req = json.loads(request.body)
        l_stateId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        l_message = req['message']
        ##print("l_state")
        #l_state = States[l_stateId]
        try:
            l_state = State.objects.get(userId=l_stateId)
        except State.DoesNotExist:
            l_state = None
			
        python_dict = literal_eval(l_state.__str__())
        ##print("l_state")
        ##print(l_state);
        #l_result = call.robust_match(l_message, l_state, 1)
        l_result = call.robust_match(l_message, python_dict, 1)
        #States[l_stateId] = l_state 
        State.objects.filter(userId=l_stateId).update(current=python_dict)
		
        #print (">>>>>>> ROBUST >>>>>>> States[l_stateId] : %s" % States[l_stateId])
        		
        return Response(l_result)