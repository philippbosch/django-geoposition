from django.shortcuts import render
from .models import PointOfInterest

def poi_list(request):
    pois = PointOfInterest.objects.all()
    return render(request, 'poi_list.html', {'pois': pois})
