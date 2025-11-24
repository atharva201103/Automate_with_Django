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
    all_models = get_all_custom_models()

    if request.method == "POST":
        csv_file = request.FILES.get("filepath")
        model_name = request.POST.get("model_name")

        if csv_file and model_name:

            import io, csv

            # read CSV in memory
            decoded = csv_file.read().decode('utf-8')

            # validate CSV header using your existing function
            try:
                check_csv_file(csv_file.name, model_name)
            except Exception as e:
                messages.error(request, str(e))
                return redirect('importdata')

            # send CSV content to Celery
            celery_import_data.delay(decoded, model_name)

            messages.success(request, "Your data is being imported, you will be notified once it is done")
            return redirect('importdata')

    context = {"all_models": all_models}
    return render(request, "dataentry/importdata.html", context)


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
