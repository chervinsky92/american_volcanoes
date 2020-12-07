import folium
import pandas as pd

data = pd.read_csv('Volcanoes.txt')
lat = list(data['LAT'])
lon = list(data['LON'])
elev = list(data['ELEV'])
name = list(data['NAME'])


def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    elif elevation > 3000:
        return 'red'
    
# iframe html for volanoes
html = """<h4>Volcano name:</h4>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=[42, -115], zoom_start=5, tiles="Stamen Terrain")

# Feature group 1 : volanoes
fgv = folium.FeatureGroup(name="Volcanoes")

# Create circle markers representing volanoes
for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe), radius=6, fill_color=color_producer(el), color='grey', fill=True, fill_opacity=0.7))

# Feature group 2 : population
fgp = folium.FeatureGroup(name="Population")

# Add a polygon layer to represent population size of countries
fgp.add_child(folium.GeoJson(data=open('world.json', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000 
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red' }))

# Add feature groups to map
map.add_child(fgv)
map.add_child(fgp)

# Add layer control to toggle feature groups on map
map.add_child(folium.LayerControl())

map.save("map.html")