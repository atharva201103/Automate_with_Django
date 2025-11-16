from django.urls import path
from .views import *

urlpatterns = [
    path("dataentry/",importdata_view,name="importdata")
]