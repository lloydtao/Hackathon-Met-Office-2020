from django.shortcuts import render

from .models import Cyclone

# Create your views here.
def index(request):
    context = {}
    cyclones = Cyclone.objects.all()
    context["cyclones"] = cyclones
    return render(request, "cycloneapp/index.html", context)

def upload_cyclones(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
    
    with csv_file.open() as file:
        csv_data = file.read()

        # Send to Lewis' csv -> python function

    return render(request, "cycloneapp/cyclone_upload.html")