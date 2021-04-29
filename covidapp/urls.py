from django.contrib import admin
from django.urls import path

from covidapp.views import index

urlpatterns = [
  path('',index),
]