from django.urls import path

from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token 
from . import views


urlpatterns = [
    path('', views.QuasimodoPageView, name='home'),
    path('init/', views.QuasimodoInitView.as_view(), name='init'),
    path('message/', views.QuasimodoMessageView.as_view(), name='message'),
	path('robust/', views.QuasimodoRobustView.as_view(), name='robust'),    
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]