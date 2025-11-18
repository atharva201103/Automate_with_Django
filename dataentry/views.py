from django.shortcuts import render,redirect
from .utils import get_all_custom_models
from upload.models import Uploadfile
from django.conf import settings
from django.core.management import call_command
from .management.commands import importdata
from django.contrib import messages
from .tasks import celery_import_data,celery_export_data
from .utils import check_csv_file
from django.http import HttpResponse

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
            #csv header_check
            try:
                check_csv_file(absolute_path,model_name)
            except Exception as e:
                messages.error(request,str(e))
                return redirect('importdata')


            #trigger the command
            celery_import_data.delay(absolute_path,model_name)
            messages.success(request,"Your data is being import, You will be notified once it is done")
           
    context={"all_models":all_models}
    return render(request,"dataentry/importdata.html",context)

def exportdata_view(request):
    if request.method == 'POST':
        model_name = request.POST.get("model_name")
        celery_export_data.delay(model_name)

        messages.success(request, "Your data is being exported, you will be notified once it is done.")
        return redirect('exportdata')

    # GET request (load dropdown)
    all_models = get_all_custom_models()
    
    context = {
        "all_models": all_models
    }

    return render(request, "dataentry/exportdata.html", context)
