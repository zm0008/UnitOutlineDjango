from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from .models import teacher
from .forms import InputForm
from .forms import InputFormCourse
from .forms import InputFormUnit
from .forms import InputFormAssessment
from .forms import CourseForm
from .models import unit, assessment

# Create your views here.
def index(request):

    teach = teacher.objects.all()
    return render(request,"MyApp/index.html",{'content':teach})

def input_view(request):
    if request.method == "POST":
        form = InputForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = InputForm()

    return render(request, "MyApp/input.html", {"form": form})

def inputcourse_view(request):
    if request.method == "POST":
        form = InputFormCourse(request.POST)

        if form.is_valid():
            form.save()
            return redirect("course")
    else:
        form = InputFormCourse()

    return render(request, "MyApp/courseinput.html", {"form": form})

def inputunit_view(request):
    if request.method == "POST":
        form = InputFormUnit(request.POST)

        if form.is_valid():
            form.save()
            return redirect("course")
    else:
        form = InputFormUnit()

    return render(request, "MyApp/unitinput.html", {"form": form})

def inputassessment_view(request):
    if request.method == "POST":
        form = InputFormAssessment(request.POST)

        if form.is_valid():
            form.save()
            return redirect("course")
    else:
        form = InputFormAssessment()

    return render(request, "MyApp/assessmentinput.html", {"form": form})

def course_view(request):

    selected_course = None
    units = None
    assessments = None
    scaling_group = None

    if request.method == "POST":
        form = CourseForm(request.POST)

        if form.is_valid():
            selected_course = form.cleaned_data["course"]
            units = unit.objects.filter(Course=selected_course)
            scaling_group = selected_course.ScalingGroup
    else:
        form = CourseForm()

    context = {
        "form": form,
        "course": selected_course,
        "units": units,
        "assessments": assessments,
        "scaling_group": scaling_group
    }
    return render(request, "MyApp/course.html", context)
