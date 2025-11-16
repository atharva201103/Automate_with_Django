from django.core.management.base import BaseCommand
from django.apps import apps
import csv
from django.contrib import messages
from django.db.utils import DataError

class Command(BaseCommand):
    help = "Import CSV data into selected model"

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str, help="CSV file path")
        parser.add_argument("model_name", type=str, help="Model name")

    def handle(self, *args, **kwargs):
        filepath = kwargs["filepath"]
        model_name = kwargs["model_name"]

        # Locate model dynamically
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = app_config.get_model(model_name)
                break
            except LookupError:
                continue

        if model is None:
            self.stdout.write(self.style.ERROR(f"Model '{model_name}' not found."))
            return
        
        model_field=[field.name for field in model._meta.fields if field.name!="id"]



        # Read CSV
        with open(filepath, "r") as file:
            reader = csv.DictReader(file)
            file_header=reader.fieldnames
            if model_field!=file_header:
                raise DataError("Field names are not matching")
            for row in reader:
                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS(f"Data imported into {model_name} successfully."))
