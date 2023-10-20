# Importamos las bibliotecas necesarias
import pandas as pd
import folium
import networkx as nx

# Interfaz de Usuario
while True:
    print("\nMenú:")
    print("1. Mostrar el mapa con el grafo original.")
    print("2. Mostrar la información de los 10 aeropuertos cuyos caminos mínimos desde el vértice dado sean los más largos.")
    print("3. Mostrar el camino mínimo entre el primer y el segundo vértice sobre el mapa de la interfaz gráfica.")
    print("4. Salir")
    opcion = input("Selecciona una opción: ")

    if opcion == '1':
        # Cargamos y limpiamos los datos
        data = pd.read_csv("flights_final_with_distance.csv")

        # Creamos un mapa
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
            #folium.PolyLine([coord1, coord2], color='blue', weight=2.5, opacity=1.0, line_cap='round', popup=f"Distance: {row['Distance (km)']} km").add_to(m)
            folium.PolyLine([coord1, coord2], color='blue', weight=2.5, opacity=1.0, line_cap='round', tooltip=f"Distance: {distance} km").add_to(m)
        
        print("A continuacaión se esta generando un archivo HTML, una vez este listo, ejecutelo para visualizar el mapa con el grafo.")
        print("Por favor espere...")
        
        # Guardamos el mapa
        m.save('airports_map_with_graph.html')
        m

    if opcion == '2':
        # Cargamos los datos en un DataFrame
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

    #if opcion == '3':

    if opcion == '4':
        print("Saliendo del programa. ¡Hasta luego!")
        break
           

