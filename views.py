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
import json
import uuid
import sys
import dante.python.lite_call_runtime_top as call
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

States ={};

def DantePageView(request):
    return HttpResponse('Hello, Dante!')

	
class DanteInitView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request): 
        model = State
        l_newState = call.init_basic()
        State.objects.create(current=l_newState)
		l_stateId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        States[l_stateId] = l_newState
        l_result = {'stateId':l_stateId, 'state':l_newState}
        return Response(l_result)
    
class DanteMessageView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        
        req = json.loads(request.body)
        l_stateId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        l_message = req['message']
        l_state = States[l_stateId]
        l_result = call.message_and_state_to_message(l_message, l_state)    
        
        return Response(l_result)

class DanteRobustView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        
        req = json.loads(request.body)
        l_stateId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        l_message = req['message']
        l_state = States[l_stateId]
        l_result = call.robust_match(l_message, l_state, 1)    
        
        return Response(l_result)