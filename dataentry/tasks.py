from awd_main.celery import app
from django.core.management import call_command
import time
from django.conf import settings
from django.core.mail import EmailMessage
from .utils import send_email_notification,generate_csv
@app.task
def celery_task():
    time.sleep(5)
    mail_subject='Test Subject'
    message='This is a test mail'
    to_email=settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject,message,to_email)
    return "Email Send Successfully"

@app.task
def celery_import_data(csv_content, model_name):
    import csv, io
    from django.apps import apps

    reader = csv.DictReader(io.StringIO(csv_content))

    # find model across ALL apps
    Model = None
    for app_config in apps.get_app_configs():
        try:
            Model = app_config.get_model(model_name)
            break
        except LookupError:
            continue

    if Model is None:
        raise ValueError(f"Model '{model_name}' not found")

    # insert rows
    for row in reader:
        Model.objects.create(**row)

    # send email
    mail_subject = 'Imported Data Completed'
    message = 'Data Imported Successfully'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email)

    return "Data Imported successfully"



@app.task
def celery_export_data(model_name):
    try:
        file_path=generate_csv(model_name)
        call_command('exportdata',model_name,file_path)    
    except Exception as e:
        raise e
    
    mail_subject='Data exported Completed'
    message='Data Exported Sucessfully'
    to_email=settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject,message,to_email,attachment=file_path)
    return "Data Exported successfully"