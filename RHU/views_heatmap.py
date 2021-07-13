from django.shortcuts import render
from .models import MorbidityReport
import folium
import branca
import pandas as pd
import sqlite3
from folium import plugins
from branca.element import Template, MacroElement


def heatmap(request):
    data_list = MorbidityReport.objects.all()
    data_list = MorbidityReport.objects.values_list('latitude', 'longitude', 'cases')

    map1 = folium.Map(location=[11.1787,122.8310], 
                     tiles='OpenStreetMap', zoom_start=14)
   

    plugins.HeatMap(data_list, radius=15, gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'}).add_to(map1)
    plugins.Fullscreen(position='topright').add_to(map1)
    map1 = map1._repr_html_()
    
    context = {
        'map1': map1
    }

    return render(request, 'Thesis/heatmap/heatmap.html', context)