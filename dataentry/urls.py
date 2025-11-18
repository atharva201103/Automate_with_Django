from django.urls import path
from .views import *

urlpatterns = [
    path("dataentry/",importdata_view,name="importdata"),
    path("exportdata/",exportdata_view,name="exportdata"),
]