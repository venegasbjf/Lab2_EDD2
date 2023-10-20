# Paso 1: Importar las bibliotecas necesarias
import pandas as pd
import folium

# Paso 2: Cargar y limpiar los datos
data = pd.read_csv("flights_final_with_distance.csv")

# Paso 3: Crear un mapa
m = folium.Map(location=[data['Source Airport Latitude'].mean(), data['Source Airport Longitude'].mean()], zoom_start=2)

# Paso 4: Agregar marcadores para cada aeropuerto
unique_airports = data.drop_duplicates(subset=['Source Airport Code'])
for index, row in unique_airports.iterrows():
    folium.Marker(
        location=[row['Source Airport Latitude'], row['Source Airport Longitude']],
        popup=row['Source Airport Name'],
    ).add_to(m)

# Paso 5: Agregar las aristas del grafo al mapa como polilíneas usando la distancia presente en el conjunto de datos
for index, row in data.iterrows():
    airport1 = row['Source Airport Code']
    airport2 = row['Destination Airport Code']
    distance = row['Distance (km)'] 

    coord1 = (row['Source Airport Latitude'], row['Source Airport Longitude'])
    coord2 = (row['Destination Airport Latitude'], row['Destination Airport Longitude'])
    #folium.PolyLine([coord1, coord2], color='blue', weight=2.5, opacity=1.0, line_cap='round', popup=f"Distance: {row['Distance (km)']} km").add_to(m)
    folium.PolyLine([coord1, coord2], color='blue', weight=2.5, opacity=1.0, line_cap='round', tooltip=f"Distance: {distance} km").add_to(m)

# Paso 6: Guardar o mostrar el mapa
m.save('airports_map_with_graph.html')
# O muestra el mapa en tu entorno de desarrollo
m
