from django import forms
from .models import teacher
from .models import course

class InputForm(forms.ModelForm):
    class Meta:
        model = teacher
        fields = ['Name', 'Area']

class CourseForm(forms.Form):
    course = forms.ModelChoiceField(queryset=course.objects.all(), label="Select Course")