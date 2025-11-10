from django.core.management.base import BaseCommand
from dataentry.models import Student
class Command(BaseCommand):
    help="Inserts sample data into the database"

    def handle(self,*args,**kwargs):
        dataset=[
            {"roll_number":"B22002","name":"Aryan Gaikwad","dept":"CSE"},  
        ]
        for data in dataset:
            existing=Student.objects.filter(roll_number=data['roll_number']).exists()
            if not existing:
                Student.objects.create(roll_number=data['roll_number'],name=data['name'],dept=data['dept'])
            else:
                self.stdout.write(self.style.SUCCESS(f"student with roll number {data['roll_number']} already exists"))
        self.stdout.write(self.style.SUCCESS("sample data inserted successfully"))
