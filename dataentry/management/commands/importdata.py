from django.core.management.base import BaseCommand
from django.apps import apps
import csv
from django.contrib import messages
from django.db.utils import DataError
from ...utils import check_csv_file
import  io

class Command(BaseCommand):
    help = "Import CSV data into selected model"

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str, help="CSV file path")
        parser.add_argument("model_name", type=str, help="Model name")

    def handle(self, *args, **kwargs):
        filepath = kwargs["filepath"]
        model_name = kwargs["model_name"]

        # find model dynamically
        Model = None
        for app_config in apps.get_app_configs():
            try:
                Model = app_config.get_model(model_name)
                break
            except LookupError:
                continue

        if Model is None:
            raise ValueError(f"Model '{model_name}' not found")

        # read file
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS(f"Data imported into {model_name} successfully."))

