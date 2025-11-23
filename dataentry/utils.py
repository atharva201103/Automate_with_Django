from django.apps import apps
from django.core.management import CommandError
import csv
from django.db import DataError
from django.conf import settings
from django.core.mail import EmailMessage
from datetime import datetime
import os
def get_all_custom_models():
    built_in_models=['Permission','LogEntry','Group','User','ContentType','Uploadfile','Session']
    custom_models=[]
    for model in apps.get_models():
        if model.__name__ not in built_in_models:
            custom_models.append(model.__name__)
    return custom_models

def check_csv_file(file_path,model_name):
    model=None
    for app_config in apps.get_app_configs():
        try:
            model=apps.get_model(app_config.label,model_name)
        except LookupError:
            continue
    if model is None:
        raise CommandError(f"model name {model_name} not found")
    
    fields=[field.name for field in model._meta.fields if field.name!="id"]

    try:
        with open(file_path,'r') as file:
            reader=csv.DictReader(file)
            header=reader.fieldnames
            if header!=fields:
                raise DataError(f"CSV file does not match with {model_name} table fields")
    except Exception as e:
        raise e
    
    return model


def send_email_notification(mail_subject,message,to_email,attachment=None):
    try:
        from_email=settings.DEFAULT_FROM_EMAIL
        if isinstance(to_email, (list, tuple)):
            to_email = list(to_email)
        else:
            to_email = [to_email]
        mail=EmailMessage(mail_subject,message,from_email,to=to_email)
        if attachment is not None:
            mail.attach_file(attachment)
        mail.send()
    except Exception as e:
        raise e


def generate_csv(model_name):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    export_dir = os.path.join(settings.MEDIA_ROOT, "exported_data")
    os.makedirs(export_dir, exist_ok=True)

    file_name = f"exported_{model_name}_data_{timestamp}.csv"
    file_path = os.path.join(export_dir, file_name)

    return file_path
