import gspread
from logging import raiseExceptions
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from datetime import datetime
from .models import teacher
from .forms import InputForm
from .forms import InputFormCourse
from .forms import InputFormUnit
from .forms import InputFormAssessment
from .forms import CourseForm
from .models import unit, assessment
from pypdf import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from django.http import FileResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from io import BytesIO
from django.shortcuts import render
from .forms import UploadFileForm
from pathlib import Path

# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file


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

def generate_pdf(data, selected_label):

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    selected_data = None

    #gets the correct row based on the users selection
    for row in data:
        if len(row) >= 6:
            label = f"{row[0]} - {row[1]} - {row[2]}"

            if label == selected_label:
                selected_data = row
                break

    #puts tetx from columns D, E and F on pdf
    y = 750
    if selected_data:
        p.drawString(50, y, f"Unit Descriptor: {selected_data[3]}")
        y -= 20
        p.drawString(50, y, f"Unit Goals: {selected_data[4]}")
        y -= 20
        p.drawString(50, y, f"Content Descriptions: {selected_data[5]}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

def upload_file(request):

    #this the code for accesing the google sheet
    location = Path(settings.BASE_DIR)/"MyApp"/"service_account.json"
    gc = gspread.service_account(filename=str(location))
    sheet = gc.open("BSSS Course Data")
    data = sheet.sheet1.get("A2:F20")

    #defines the choices for the form, using ABC as label
    choices = [
        (f"{row[0]} - {row[1]} - {row[2]}", f"{row[0]} - {row[1]} - {row[2]}")
        for row in data
        if len(row) >= 3
    ]

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        form.fields["selection"].choices = choices

        if form.is_valid():
            selected_label = form.cleaned_data["selection"]
            pdf_file = request.FILES.get("file")
            
            merger = PdfWriter()
            input1 = PdfReader(generate_pdf(data, selected_label))

            try:
                merger.append(input1)
                if pdf_file:
                    input2 = PdfReader(pdf_file, "rb")
                    merger.append(input2)
                buffer = BytesIO()
                merger.write(buffer)
                buffer.seek(0)
                response = FileResponse(buffer, as_attachment=True, filename="Attachment.pdf")

            except FileNotFoundError:
                response = FileResponse(generate_pdf(), as_attachment=True, filename="noAttachment.pdf")
            return response
    else:
        form = UploadFileForm()
        form.fields["selection"].choices = choices  
    return render(request, "MyApp/upload.html", {"form": form})
