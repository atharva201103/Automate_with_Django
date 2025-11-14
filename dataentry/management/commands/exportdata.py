import csv
from django.core.management.base import BaseCommand
from django.apps import apps
import datetime

class Command(BaseCommand):
    help="export student data to csv file"

    def add_arguments(self,parser):
        parser.add_argument("model_name",type=str,help="name of the model to export data")

    def handle(self,*args,**kwargs):
        model_name=kwargs['model_name'].capitalize()
        model=None
        for app_config in apps.get_app_configs():
            try:
                model=apps.get_model(app_config.label,model_name)
                break
            except LookupError:
                pass
        if model is None:
            self.stderr.write(f"Model {model_name} not found in any installed app")
            return 
        else:
            data=model.objects.all()
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            filename=f"Exported_{model_name}_{timestamp}.csv"
            with open(filename,'w',newline='') as file:
                writer=csv.writer(file)
                writer.writerow([field.name for field in model._meta.fields])
                for obj in data:
                    writer.writerow([getattr(obj,field.name) for field in model._meta.fields])
        self.stdout.write(self.style.SUCCESS(f"{model_name} data exported successfully to {filename}"))

            
