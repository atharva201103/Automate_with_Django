from django.db import models

# Create your models here.
class Student(models.Model):
    roll_number=models.CharField(max_length=10)
    name=models.CharField(max_length=100)
    dept=models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
    
class Customer(models.Model):
    customer_name=models.CharField(max_length=50)
    country=models.CharField(max_length=50)

    def __str__(self):
        return f"{self.customer_name}"