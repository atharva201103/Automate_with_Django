from django.shortcuts import render
from dataentry.tasks import celery_task
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return render(request, "home.html")

def celery_task_test(request):
    celery_task.delay()
    return HttpResponse('<h3>Task Completed Successfully</h3>')

