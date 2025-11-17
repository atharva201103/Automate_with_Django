from awd_main.celery import app
from django.core.management import call_command
import time
from django.conf import settings
from django.core.mail import EmailMessage
from .utils import send_email_notification
@app.task
def celery_task():
    time.sleep(5)
    mail_subject='Test Subject'
    message='This is a test mail'
    to_email=settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject,message,to_email)
    return "Email Send Successfully"

@app.task
def celery_import_data(absolute_path,model_name):
    try:
        call_command('importdata',absolute_path,model_name)    
    except Exception as e:
        raise 
    mail_subject='Imported Data Completed'
    message='Data Imported Sucessfully'
    to_email=settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject,message,to_email)
    return "Data Imported successfully"

       


