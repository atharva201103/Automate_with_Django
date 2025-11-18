import csv
from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = "Export model data to CSV file"

    def add_arguments(self, parser):
        parser.add_argument("model_name", type=str)
        parser.add_argument("file_path", type=str)  # <- MUST be here

    def handle(self, *args, **kwargs):
        model_name = kwargs["model_name"].capitalize()
        file_path = kwargs["file_path"]              # <- MUST use this path

        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue

        if model is None:
            self.stderr.write(f"Model {model_name} not found")
            return

        data = model.objects.all()
        fields = [field.name for field in model._meta.fields]

        # Write CSV to the EXACT file_path created in generate_csv()
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            for obj in data:
                writer.writerow([getattr(obj, field) for field in fields])

        self.stdout.write(self.style.SUCCESS(
            f"{model_name} data exported successfully to {file_path}"
        ))
