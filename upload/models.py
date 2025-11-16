from django.db import models

# Create your models here.
class Uploadfile(models.Model):
    upload_file=models.FileField(upload_to="upload/")
    model_name=models.CharField(max_length=100)
    upload_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model_name