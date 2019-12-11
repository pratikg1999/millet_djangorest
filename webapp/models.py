from django.db import models

# Create your models here.
class Employee(models.Model):
    firstName = models.CharField(max_length=10)
    lastName = models.CharField(max_length=10)
    empId = models.IntegerField()

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

class File(models.Model):
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name   