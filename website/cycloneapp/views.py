import csv

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import dateparse

from .models import Cyclone, CycloneNode
from .storms_with_query import query_storms
from .storms import storm_query_slow


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
    # return JsonResponse(query_storms(date_range, click_long, click_lat, radius))
    return JsonResponse(storm_query_slow(date_range, click_lat, click_long, radius))


def upload_cyclones(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]

        with open(csv_file.temporary_file_path(), encoding="utf-8") as file:
            # Send to Lewis' csv -> python function
            cyclone_data = csv.reader(file, delimiter=",")
            current_sid = None
            current_cyclone = None
            
            firstPass = True

            for counter, raw_cyclone in enumerate(cyclone_data, 0):
                if firstPass:
                    firstPass = False
                    continue

                intensity = raw_cyclone[6]
                intensity = None if intensity == " " else intensity

                if intensity == None or intensity == "": continue

                if current_sid != raw_cyclone[0] or current_sid is None:
                    current_sid = raw_cyclone[0]
                    datetime = dateparse.parse_datetime(raw_cyclone[5])

                    # print(raw_cyclone[5])
                    # print(datetime)
                    current_cyclone, created = Cyclone.objects.get_or_create(
                        sid=raw_cyclone[0],
                        name=raw_cyclone[2],
                        datetime=datetime
                    )
                    current_cyclone.save()
    
                cyclone_node, created = CycloneNode.objects.get_or_create(
                    cyclone=current_cyclone,
                    time_index=raw_cyclone[1],
                    lat=raw_cyclone[3],
                    long=raw_cyclone[4],
                    intensity=intensity
                )
                cyclone_node.save()

                if counter % 300 == 0:
                    print(f"{counter} processed")

    print(f"CSV upload done, {len(Cyclone.objects.all())} items processed")

    return render(request, "cycloneapp/cyclone_upload.html")