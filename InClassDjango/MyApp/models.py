from django.db import models

# Create your models here.a
class teacher(models.Model):
    Name = models.CharField(max_length=25)
    Area = models.CharField(max_length=30)

class unit(models.Model):
    Name = models.CharField(max_length=30)

class assessment(models.Model):
    Unit = models.ForeignKey(unit, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    StartDate = models.DateField()
    DueDate = models.DateField()



