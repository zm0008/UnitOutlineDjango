from django import forms
from .models import teacher
from .models import course
from .models import assessment
from .models import unit
from .models import scalinggroup

class InputForm(forms.ModelForm):
    class Meta:
        model = teacher
        fields = ['Name', 'Area', 'Courses']

class InputFormCourse(forms.ModelForm):
    class Meta:
        model = course
        fields = ['Name', 'ScalingGroup']

class InputFormUnit(forms.ModelForm):
    class Meta:
        model = unit
        fields = ['Name', 'Course']

class InputFormAssessment(forms.ModelForm):
    class Meta:
        model = assessment
        fields = ['Name', 'Unit', 'StartDate', 'DueDate']

class InputFormScalingGroup(forms.ModelForm):
    class Meta:
        model = scalinggroup
        fields = ['Name']

class CourseForm(forms.Form):
    course = forms.ModelChoiceField(queryset=course.objects.all(), label="Select Course")