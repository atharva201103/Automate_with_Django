from django.contrib import admin
from .models import Uploadfile

# Register your models here.
class Uploadfileadmin(admin.ModelAdmin):
    list_display=["model_name","upload_time"]
admin.site.register(Uploadfile,Uploadfileadmin)