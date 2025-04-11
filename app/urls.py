from operator import index

from django.urls import path

from Lost_Found_Pets.urls import urlpatterns
from . import views
from .views import UserView, RegisterUser

#from .views import new_user

urlpatterns = [
    path('',index,name='index'),



]