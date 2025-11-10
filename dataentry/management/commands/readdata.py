from django.core.management.base import BaseCommand
from dataentry.models import Student,Customer
import csv
from django.apps import apps
class Command(BaseCommand):
    help="reads data from csv file"

    def add_arguments(self, parser):
        parser.add_argument("filepath",type=str,help='path to read data from csv file')
        parser.add_argument("model_name",type=str,help='name of the model')
    def handle(self,*args,**kwargs):
        filepath=kwargs['filepath']
        model_name=kwargs['model_name'].capitalize()
        model = None
        for app_config in apps.get_app_configs():
            try:
                model=app_config.get_models(app_config.label,model_name)
                break
            except LookupError:
                continue
        if model is None:
            self.stdout.write(self.style.ERROR(f"Model '{model_name}' not found in any installed app."))
        if model_name=='Student':
            with open(filepath,'r') as file:
                reader=csv.DictReader(file)
                for row in reader:
                    exist=Student.objects.filter(roll_number=row['roll_number']).exists()
                    if not exist:
                        Student.objects.create(
                            roll_number=row['roll_number'],
                            name=row['name'],
                            dept=row['dept']
                        )
                    else:
                        self.stdout.write(self.style.SUCCESS(f"student with roll number {row['roll_number']} already exists"))
            self.stdout.write(self.style.SUCCESS("data read from csv file successfully"))
        else:
            with open(filepath,'r') as file:
                reader=csv.DictReader(file)
                for row in reader:
                        Customer.objects.create(
                            customer_name=row['customer_name'],
                            country=row['country']
                        )            
            self.stdout.write(self.style.SUCCESS("data read from csv file successfully"))
        
        

        