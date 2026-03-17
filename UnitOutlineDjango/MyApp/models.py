from django.db import models

# Create your models here.a


class scalinggroup(models.Model):
    Name = models.IntegerField()

class course(models.Model):
    Name = models.CharField(max_length=20)
    ScalingGroup = models.ForeignKey(scalinggroup, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.Name

class teacher(models.Model):
    Name = models.CharField(max_length=25)
    Area = models.CharField(max_length=30)
    Courses = models.ManyToManyField(course, blank=True)

    def __str__(self):
        return self.Name

class unit(models.Model):
    Name = models.CharField(max_length=30)
    Course = models.ForeignKey(course, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name

class assessment(models.Model):
    Unit = models.ForeignKey(unit, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    StartDate = models.DateField()
    DueDate = models.DateField()

    def __str__(self):
        return self.Name

class student(models.Model):
    Tertiary = "T"
    Accredited = "A"

    PACKAGETYPES = [
        (Tertiary, "Tertiary"), 
        (Accredited, "A")
    ]

    Name = models.CharField(max_length=25)
    Courses = models.ManyToManyField(course)
    PackageType = models.CharField(max_length=1, choices=PACKAGETYPES)
