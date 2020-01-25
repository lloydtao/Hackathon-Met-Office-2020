from django.shortcuts import render

from .models import Cyclone

# Create your views here.
def index(request):
    context = {}
    cyclones = Cyclone.objects.all()

    # 1950 and 1970
    ranged_cyclones = Cyclone.objects.filter(date__range=["1950-01-01", "1970-01-01"])
    
    context["cyclones"] = cyclones

    return render(request, "cycloneapp/index.html", context)

def upload_cyclones(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
    
    with csv_file.open() as file:
        csv_data = file.read()

        # Send to Lewis' csv -> python function

    return render(request, "cycloneapp/cyclone_upload.html")