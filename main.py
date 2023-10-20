# Importamos las bibliotecas necesarias
import pandas as pd
import folium
import networkx as nx

# Cargamos los datos
data = pd.read_csv("flights_final_with_distance.csv")

# Creamos un grafo dirigido con NetworkX
G = nx.DiGraph()

# Agregamos nodos (aeropuertos) y aristas (rutas) al grafo
for index, row in data.iterrows():
    G.add_edge(row['Source Airport Code'], row['Destination Airport Code'], weight=row['Distance (km)'])

# Función para encontrar los 10 caminos más largos desde un vértice dado
def find_longest_paths(graph, source_node):
    paths = nx.single_source_dijkstra_path_length(graph, source_node)
    sorted_paths = sorted(paths.items(), key=lambda x: x[1], reverse=True)
    return sorted_paths[:10]

# Función para obtener detalles de un aeropuerto dado su código
def get_airport_details(airport_code):
    airport_info = data[data['Source Airport Code'] == airport_code]
    return airport_info.iloc[0]

# Interfaz de Usuario
while True:
    print("\nMenú:")
    print("1. Mostrar el mapa con el grafo original.")
    print("2. Mostrar la información de los 10 aeropuertos cuyos caminos mínimos desde el vértice dado sean los más largos.")
    print("3. Camino mínimo entre dos vértices")
    print("4. Salir")
    opcion = input("Selecciona una opción: ")

    if opcion == '1':
        # Creamos un mapa con Folium
        m = folium.Map(location=[data['Source Airport Latitude'].mean(), data['Source Airport Longitude'].mean()], zoom_start=2)

        # Agregamos marcadores para cada aeropuerto
        unique_airports = data.drop_duplicates(subset=['Source Airport Code'])
        for index, row in unique_airports.iterrows():
            folium.Marker(
                location=[row['Source Airport Latitude'], row['Source Airport Longitude']],
                popup= [row['Source Airport Code'], row['Source Airport Name'], 
                        row['Source Airport City'], row['Source Airport Country'], row['Source Airport Latitude'], row['Source Airport Longitude']]
            ).add_to(m)

        # Agregamos las aristas del grafo al mapa como polilíneas usando la distancia presente en el conjunto de datos
        for index, row in data.iterrows():
            airport1 = row['Source Airport Code']
            airport2 = row['Destination Airport Code']
            distance = row['Distance (km)']

            coord1 = (row['Source Airport Latitude'], row['Source Airport Longitude'])
            coord2 = (row['Destination Airport Latitude'], row['Destination Airport Longitude'])
            folium.PolyLine([coord1, coord2], color='red', weight=2.5, opacity=1.0, line_cap='round', tooltip=f"Distance: {distance} km").add_to(m)
        
        print("A continuación se está generando un archivo HTML, una vez esté listo, ejecútelo para visualizar el mapa con el grafo.")
        print("Por favor espere...")
        
        # Guardamos el mapa como un archivo HTML
        m.save('airports_map_with_graph.html')

    elif opcion == '2':
        # Ingresamos el código del aeropuerto de inicio
        start_airport_code = input("Ingresa el código del aeropuerto de inicio: ")

        if start_airport_code in G.nodes:
            longest_paths = find_longest_paths(G, start_airport_code)
            
            # Mostramos los 10 caminos más largos y sus detalles
            print("Los 10 caminos más largos desde el aeropuerto", start_airport_code, "son:")
            for i, (airport, distance) in enumerate(longest_paths, 1):
                airport_details = get_airport_details(airport)
                print(f"{i}. Código: {airport_details['Source Airport Code']}, Nombre: {airport_details['Source Airport Name']}, Ciudad: {airport_details['Source Airport City']}, País: {airport_details['Source Airport Country']}, Latitud: {airport_details['Source Airport Latitude']}, Longitud: {airport_details['Source Airport Longitude']}, Distancia: {distance: .2f} Km")
        else:
            print("El código del aeropuerto de inicio no se encuentra en el grafo.")

    elif opcion == '3':
        start_airport_code = input("Ingresa el código del primer aeropuerto de inicio: ")
        end_airport_code = input("Ingresa el código del segundo aeropuerto de destino: ")

        if start_airport_code in G.nodes and end_airport_code in G.nodes:
            # Encontrar el camino mínimo entre los dos vértices
            shortest_path = nx.shortest_path(G, source=start_airport_code, target=end_airport_code, weight='weight')

            # Crear un mapa con Folium
            m = folium.Map(location=[data['Source Airport Latitude'].mean(), data['Source Airport Longitude'].mean()], zoom_start=2)

            # Agregar marcadores para los aeropuertos en el camino mínimo
            for airport_code in shortest_path:
                airport_details = get_airport_details(airport_code)
                folium.Marker(
                    location=[airport_details['Source Airport Latitude'], airport_details['Source Airport Longitude']],
                    popup="Código: {}\nNombre: {}\nCiudad: {}\nPaís: {}  {}\nLatitud:  {}\nLongitud:".format(
                        airport_details['Source Airport Code'], airport_details['Source Airport Name'],
                        airport_details['Source Airport City'], airport_details['Source Airport Country'],
                         airport_details['Source Airport Latitude'], airport_details['Source Airport Longitude'])
                ).add_to(m)

            # Agregar polilíneas para representar el camino mínimo
            for i in range(len(shortest_path) - 1):
                airport1 = shortest_path[i]
                airport2 = shortest_path[i + 1]
                distance = G[airport1][airport2]['weight']

                airport1_details = get_airport_details(airport1)
                airport2_details = get_airport_details(airport2)

                coord1 = (airport1_details['Source Airport Latitude'], airport1_details['Source Airport Longitude'])
                coord2 = (airport2_details['Source Airport Latitude'], airport2_details['Source Airport Longitude'])
                folium.PolyLine([coord1, coord2], color='red', weight=2.5, opacity=1.0,
                                line_cap='round', tooltip=f"Distance: {distance} km").add_to(m)

            print("Se está generando un archivo HTML, una vez esté listo, ejecútelo para visualizar el mapa con el camino mínimo.")
            print("Por favor espere...")

            # Guardamos el mapa como un archivo HTML
            m.save('shortest_path_map.html')

        else:
            print("Uno o ambos códigos de aeropuerto no se encuentran en el grafo.")
    elif opcion == "4":
        print("Saliendo del programa. ¡Hasta luego!")
        break
       
           

