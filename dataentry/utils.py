from django.apps import apps
from django.core.management import CommandError
import csv
from django.db import DataError
from django.conf import settings
from django.core.mail import EmailMessage
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


def send_email_notification(mail_subject,message,to_email):
    try:
        from_email=settings.DEFAULT_FROM_EMAIL
        mail=EmailMessage(mail_subject,message,from_email,to=[to_email])
        mail.send()
    except Exception as e:
        raise e


