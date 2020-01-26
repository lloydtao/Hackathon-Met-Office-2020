import csv

from django.shortcuts import render

from .models import Cyclone, CycloneNode
from .storms_with_query import query_storms


def index(request):
    context = {}
    cyclones = Cyclone.objects.all()

    # 1950 and 1970
    # ranged_cyclones = Cyclone.objects.filter(date__range=["1950-01-01", "1970-01-01"])
    
    context["cyclones"] = cyclones

    return render(request, "globe/index.html", context)


def freq_storms(request):
    date_range = request.GET.get("date_range")
    click_long = request.GET.get("click_long")
    click_lat = request.GET.get("click_lat")
    radius = request.GET.get("radius")
    
    # Process cyclones based on radius and date range
    query_storms(date_range, click_long, click_lat, radius)


def upload_cyclones(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]

        with open(csv_file.temporary_file_path(), encoding="utf-8") as file:
            # Send to Lewis' csv -> python function
            cyclone_data = csv.reader(file, delimiter=",")

            firstPass = True
            for raw_cyclone in cyclone_data:
                if firstPass:
                    firstPass = False
                    continue

                intensity = raw_cyclone[6]
                intensity = None if intensity == " " else intensity

                cyclone, created = Cyclone.objects.get_or_create(sid=raw_cyclone[0], name=raw_cyclone[2])
                cyclone.save()
                cyclone_node, created = CycloneNode.objects.get_or_create(
                    cyclone=cyclone,
                    time_index=raw_cyclone[1],
                    lat=raw_cyclone[3],
                    long=raw_cyclone[4],
                    intensity=intensity
                )
                cyclone_node.save()

    print(f"CSV upload done, {len(Cyclone.objects.all())} items processed")

    return render(request, "cycloneapp/cyclone_upload.html")