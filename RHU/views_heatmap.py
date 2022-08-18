from tokenize import String
from django.shortcuts import render
from django.db.models import Count, Sum, Max
from markupsafe import string

from Thesis.settings import DATABASE_PATH
from .models import MorbidityReport
from geopy.geocoders import Nominatim
import folium
import branca
import pandas as pd
import numpy as np
import sqlite3
import re
import fileinput
from folium import plugins
from branca.element import Template, MacroElement


def heatmap(request):

    comm = MorbidityReport.objects.filter(classification='Communicable Disease')
    comm = MorbidityReport.objects.values_list('latitude', 'longitude')

    noncomm = MorbidityReport.objects.filter(classification='Non-communicable Disease')
    noncomm = MorbidityReport.objects.values_list('latitude', 'longitude')

    map1 = folium.Map(location=[11.1787,122.8310], 
                     tiles='OpenStreetMap', zoom_start=14)
   
    tooltip = "Click for more info!"

    conn = sqlite3.connect(r'C:\Users\Einre Paul\Desktop\django\Thesis\db.sqlite3')
    db = pd.read_sql_query('SELECT * FROM RHU_morbidityreport', conn)

    pd.set_option('max_columns', None)

    communicable = folium.FeatureGroup(name = "Communicable Diseases")
    noncommunicable = folium.FeatureGroup(name= "Non-communicable Diseases")

    for v,y in db.iterrows():

        classification = (y['classification'])
        barangay = (y['barangay'])
        disease = (y['disease'])
        cases = (y['cases'])

        for disease in barangay:
            popup = """
            Disease: <b>%s</b> - %s </br>
            """ % (y['disease']), (y['cases'])

        popup1 = "Aripdip"
        popup2 = "Calaigang"
        popup3 = "Ilongbukid"
        popup4 = "Poscolon"
        popup5 = "San Florentino"
    
        if classification == 'C':
            for x in comm:
                if barangay == 'Aripdip':
                    folium.Marker(location=[x[0],x[1]], tooltip = tooltip, popup = popup, icon = folium.Icon(icon='fa-plus-square', prefix='fa')).add_to(communicable)
                elif barangay == 'Calaigang':
                    folium.Marker(location=[x[0],x[1]], tooltip = tooltip, popup = popup, icon = folium.Icon(icon='fa-plus-square', prefix='fa')).add_to(communicable)
                elif barangay == 'Ilongbukid':
                    folium.Marker(location=[x[0],x[1]], tooltip = tooltip, popup = popup, icon = folium.Icon(icon='fa-plus-square', prefix='fa')).add_to(communicable)
                elif barangay == 'Poscolon':
                    folium.Marker(location=[x[0],x[1]], tooltip = tooltip, popup = popup, icon = folium.Icon(icon='fa-plus-square', prefix='fa')).add_to(communicable)
                elif barangay == 'San Florentino':
                    folium.Marker(location=[x[0],x[1]], tooltip = tooltip, popup = popup, icon = folium.Icon(icon='fa-plus-square', prefix='fa')).add_to(communicable)
        if classification == 'NC':
            for x in noncomm:
                if barangay == 'Aripdip':
                    folium.Marker(location=[x[0],x[1]], tooltip = tooltip, popup = popup, icon = folium.Icon(icon='fa-plus-square', prefix='fa')).add_to(noncommunicable)
                elif barangay == 'Calaigang':
                    folium.Marker(location=[x[0],x[1]], tooltip = tooltip, popup = popup, icon = folium.Icon(icon='fa-plus-square', prefix='fa')).add_to(noncommunicable)
                elif barangay == 'Ilongbukid':
                    folium.Marker(location=[x[0],x[1]], tooltip = tooltip, popup = popup, icon = folium.Icon(icon='fa-plus-square', prefix='fa')).add_to(noncommunicable)
                elif barangay == 'Poscolon':
                    folium.Marker(location=[x[0],x[1]], tooltip = tooltip, popup = popup, icon = folium.Icon(icon='fa-plus-square', prefix='fa')).add_to(noncommunicable)
                elif barangay == 'San Florentino':
                    folium.Marker(location=[x[0],x[1]], tooltip = tooltip, popup = popup, icon = folium.Icon(icon='fa-plus-square', prefix='fa')).add_to(noncommunicable)

    communicable.add_to(map1)
    noncommunicable.add_to(map1)
    
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

    plugins.HeatMap(comm, min_opacity=0.2, radius=30, blur=20, gradient={'0': 'Navy','0.25': 'Navy', '0.26': 'Green', '0.5': 'Green', '0.51': 'Yellow', '0.75': 'Yellow', '0.76': 'Red', '1': 'Red'},max_zoom=11).add_to(map1)
    plugins.HeatMap(noncomm, min_opacity=0.2, radius=30, blur=20, gradient={'0': 'Black','0.25': 'Black','0.26': 'DarkRed','0.5':'DarkRed','0.51': 'Brown','0.75':'Brown','0.76':'Gray','1': 'Gray'},max_zoom=11).add_to(map1)
    folium.LayerControl(collapsed = False ).add_to(map1)
    map1 = map1._repr_html_()

    context = {
        'map1': map1, 
    }

    return render(request, 'Thesis/heatmap/heatmap.html', context)
