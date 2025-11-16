from django.apps import apps
def get_all_custom_models():
    built_in_models=['Permission','LogEntry','Group','User','ContentType','Uploadfile','Session']
    custom_models=[]
    for model in apps.get_models():
        if model.__name__ not in built_in_models:
            custom_models.append(model.__name__)
    return custom_models


