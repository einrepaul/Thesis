from django.shortcuts import render
from django.db.models import Count, Sum, Max
from .models import MorbidityReport
import folium
import branca
import pandas as pd
import sqlite3
from folium import plugins
from branca.element import Template, MacroElement
from folium.plugins import FloatImage


def heatmap(request):
    comm = MorbidityReport.objects.filter(classification="Communicable Disease")
    comm = MorbidityReport.objects.values_list('latitude', 'longitude')

    noncomm = MorbidityReport.objects.filter(classification="Non-communicable Disease")
    noncomm = MorbidityReport.objects.values_list('latitude', 'longitude')

    map1 = folium.Map(location=[11.1787,122.8310], 
                     tiles='OpenStreetMap', zoom_start=14)
   
    cluster = plugins.MarkerCluster().add_to(map1)

    for x in comm:
        folium.Marker(location=[x[0],x[1]]).add_to(cluster)
    
    for x in noncomm:
        folium.Marker(location=[x[0],x[1]]).add_to(cluster)
    
    totalAripdip = MorbidityReport.objects.filter(barangay='Aripdip').aggregate(Sum('cases')).get('cases__sum')
    totalIlongbukid = MorbidityReport.objects.filter(barangay='Ilongbukid').aggregate(Sum('cases')).get('cases__sum')
    totalCalaigang = MorbidityReport.objects.filter(barangay='Calaigang').aggregate(Sum('cases')).get('cases__sum')
    totalPoscolon = MorbidityReport.objects.filter(barangay='Poscolon').aggregate(Sum('cases')).get('cases__sum')
    totalSanDionisio = MorbidityReport.objects.filter(barangay='San Dionisio').aggregate(Sum('cases')).get('cases__sum')
    totalSanFlorentino = MorbidityReport.objects.filter(barangay='San Florentino').aggregate(Sum('cases')).get('cases__sum')

    cases_barangay = {
        'totalAripdip': totalAripdip,
        'totalIlongbukid': totalIlongbukid,
        'totalCalaigang': totalCalaigang,
        'totalPoscolon': totalPoscolon,
        'totalSanDionisio': totalSanDionisio,
        'totalSanFlorentino': totalSanFlorentino,
    }


    plugins.HeatMap(comm, min_opacity=0.2, max_val=1000, radius=30, blur=20, gradient={'0': 'Navy','0.25': 'Navy','0.26': 'Green','0.5':'Green','0.51': 'Yellow','0.75':'Yellow','0.76':'Red','1': 'Red'},max_zoom=11).add_to(map1)
    plugins.HeatMap(noncomm, min_opacity=0.2, max_val=1000, radius=30, blur=20, gradient={'0': 'Black','0.25': 'Black','0.26': 'DarkRed','0.5':'DarkRed','0.51': 'Brown','0.75':'Brown','0.76':'Gray','1': 'Gray'},max_zoom=11).add_to(map1)
    plugins.Fullscreen(position='topright').add_to(map1)

    image_file1 = 'comm1.PNG'

    FloatImage(image_file1, bottom=0, left=86).add_to(map1)
    
    
    map1 = map1._repr_html_()
    
    
    context = {
        'map1': map1,

    }

    



    return render(request, 'Thesis/heatmap/heatmap.html', context)
