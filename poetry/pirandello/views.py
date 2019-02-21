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
import json
import uuid
import sys
#TODO
sys.path.append('./pirandello/python/')
import pirandello.python.lite_call_runtime_top as call

States ={};

def PirandelloPageView(request):
    return HttpResponse('Hello, Pirandello!')

	
class PirandelloInitView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        
        print(request.META.get('HTTP_AUTHORIZATION').split(' ')[1])
        l_newState = call.init_basic()
        #l_newState = call.init_state('C:/Projects/django/callector/api/python/call_tables.data.gz', 'C:/Projects/django/callector/api/python/robust_matching_tables.data.gz')
        #l_newState = call.init_state('C:/Projects/django/callector/api/lite_call_python/call_tables.data.gz', 'C:/Projects/django/callector/api/lite_call_python/robust_matching_tables.data.gz')
        print("l_newState")
        print(l_newState);
        l_stateId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        #l_stateId = uuid.uuid4().hex # generate unique Id for state
        States[l_stateId] = l_newState
        l_result = {'stateId':l_stateId, 'state':l_newState}
        return Response(l_result)

class PirandelloMessageView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        
        req = json.loads(request.body)
        l_stateId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        l_message = req['message']
        #print("l_state")
        l_state = States[l_stateId]
        #print("l_state")
        #print(l_state);
        l_result = call.message_and_state_to_message(l_message, l_state)    
        
        return Response(l_result)

class PirandelloRobustView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        
        req = json.loads(request.body)
        l_stateId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        l_message = req['message']
        #print("l_state")
        l_state = States[l_stateId]
        #print("l_state")
        #print(l_state);
        l_result = call.robust_match(l_message, l_state, 1)    
        
        return Response(l_result)