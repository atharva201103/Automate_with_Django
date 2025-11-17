from django.core.management.base import BaseCommand
from django.apps import apps
import csv
from django.contrib import messages
from django.db.utils import DataError
from ...utils import check_csv_file

class Command(BaseCommand):
    help = "Import CSV data into selected model"

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str, help="CSV file path")
        parser.add_argument("model_name", type=str, help="Model name")

    def handle(self, *args, **kwargs):
        filepath = kwargs["filepath"]
        model_name = kwargs["model_name"]

        # Locate model dynamically
        model=check_csv_file(filepath,model_name)
        # Read CSV
        with open(filepath,'r') as file:
            reader=csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS(f"Data imported into {model_name} successfully."))
