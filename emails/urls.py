from django.urls import path
from .views import *

urlpatterns = [
    path("send-emails/",send_emails,name="send_email")
]
