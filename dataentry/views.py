from django.shortcuts import render
from .utils import get_all_custom_models
from upload.models import Uploadfile
from django.conf import settings
from django.core.management import call_command
from .management.commands import importdata
from django.contrib import messages

# Create your views here.
def importdata_view(request):
    all_models=get_all_custom_models()
    if request.method=="POST":
        file_path=request.FILES.get("filepath")
        model_name=request.POST.get("model_name")
        if file_path and model_name:
            upload=Uploadfile.objects.create(upload_file=file_path,model_name=model_name)
            #construct absolute path
            relative_path=str(upload.upload_file.url)
            base_url=str(settings.BASE_DIR)
            absolute_path=base_url+relative_path
            #trigger the command
            try:
                call_command('importdata',absolute_path,model_name)
                messages.success(request,"Data imported succresufully")
            except Exception as e:
                messages.error(request,e)
    context={"all_models":all_models}
    return render(request,"dataentry/importdata.html",context)