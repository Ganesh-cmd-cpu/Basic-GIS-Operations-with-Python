import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import folium

# Load shapefile or GeoJSON
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Filter for a single country
india = world[world['name'] == 'India']

# Create a point (e.g., New Delhi)
point = Point(77.2090, 28.6139)  # (Longitude, Latitude)

# Convert it to GeoSeries with CRS
point_gdf = gpd.GeoSeries([point], crs="EPSG:4326")

# Buffer around the point (100 km)
buffered = point_gdf.to_crs(epsg=3857).buffer(100000).to_crs(epsg=4326)

# Create a GeoDataFrame for buffer
buffer_gdf = gpd.GeoDataFrame(geometry=buffered)

# Plot using Matplotlib
fig, ax = plt.subplots(figsize=(8, 8))
india.plot(ax=ax, color='lightgray')
buffer_gdf.plot(ax=ax, edgecolor='red', facecolor='none', linewidth=2)
point_gdf.plot(ax=ax, color='blue')
plt.title('Buffer around New Delhi (100 km)')
plt.show()

# Create an interactive map with Folium
m = folium.Map(location=[28.6139, 77.2090], zoom_start=6)
folium.Marker([28.6139, 77.2090], popup='New Delhi').add_to(m)
folium.GeoJson(data=buffer_gdf.__geo_interface__, style_function=lambda x: {'color': 'red'}).add_to(m)

# Save map
m.save("new_delhi_buffer_map.html")
print("Map saved as new_delhi_buffer_map.html")
