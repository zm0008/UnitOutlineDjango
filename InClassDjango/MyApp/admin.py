from django.contrib import admin
from .models import teacher 
from .models import unit
from .models import assessment
# Register your models here.
admin.site.register(teacher)
admin.site.register(unit)
admin.site.register(assessment)