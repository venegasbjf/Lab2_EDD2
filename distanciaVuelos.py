import pandas as pd
from geopy.distance import great_circle

# Cargar el dataset
df = pd.read_csv('flights_final.csv')

# Función para calcular la distancia con dos decimales
def calculate_distance(row):
    source_coords = (row['Source Airport Latitude'], row['Source Airport Longitude'])
    dest_coords = (row['Destination Airport Latitude'], row['Destination Airport Longitude'])
    distance_km = great_circle(source_coords, dest_coords).kilometers
    return round(distance_km, 2)

# Calcular la distancia y agregarla como una nueva columna
df['Distance (km)'] = df.apply(calculate_distance, axis=1)

# Guardar el dataset con la nueva columna
df.to_csv('flights_final_with_distance.csv', index=False)
