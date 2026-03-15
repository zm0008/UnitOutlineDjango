from django.contrib import admin
from .models import teacher 
from .models import unit
from .models import assessment
from .models import scalinggroup
from .models import student
from .models import course
# Register your models here.
admin.site.register(teacher)
admin.site.register(unit)
admin.site.register(assessment)
admin.site.register(scalinggroup)
admin.site.register(student)
admin.site.register(course)