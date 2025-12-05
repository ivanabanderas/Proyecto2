from grafo import graph
from pyproj import Transformer
from exhaustive import exhaustive
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time
import osmnx as ox
import random
from kdTree import build_kd_tree, nearest

#Componente 1
G, points, node_ids = graph("Av. Mariano Otero 3000, Jardines del Sol, 45050 Zapopan, Jal.", dist=10000)


print("\nConstruyendo KD-tree...")
start = time.time()
root = build_kd_tree(points.tolist(), node_ids, depth=0)
end = time.time()
kdTree_time = end - start

lista_de_hospitales = [
    (20.650105413559686, -103.40617560813115), #Hospital Geria
    (20.645279706184876, -103.4337500405164), #Hospital el colli
    (20.650567336520627, -103.38733504404179), #Hospital auxiliadora
    (20.643407372920343, -103.38272774452646), #Hospital de la cruz
    (20.634091216748587, -103.41456747510544), #Cruz verde las aguilas
    (20.629933409227878, -103.41876340859261), #Hospital de Paua
    (20.62754646840088, -103.42131387796714), #Hospital mision san Felipe
    (20.63139635445717, -103.42378207413606), #Hospital arboledas
    (20.65015289935685, -103.38663974029575), #Hospital auxiliadora
    (20.66161357522582, -103.39538833227856), #Hospital toledo guadalajara
    (20.667834723010163, -103.40894864985191), #Hospital Santa María Chapalita
    (20.66554275083613, -103.42014684758993), #Hospital jardines
    (20.66650430517377, -103.38934645585044), #Hospital CHG
    (20.674183331828086, -103.41038516849666), #hospital real san josé
    (20.680557697537616, -103.39858364470734), #Hospital anegeles del carmen
    (20.68538281842212, -103.38665591593572), #hospital terranova
]

transformer = Transformer.from_crs(4326, 32613, always_xy=True)

#En esta seccion se aplica el componente 1, para la creacion y busqueda de los nodos mas cercanos a los puntos dados en latitud y longitud

coords_20_utm = []
for lat, lon in lista_de_hospitales:
    x, y = transformer.transform(lon, lat)
    coords_20_utm.append((x, y))

nearest_results = []
kd_times = []

for t in coords_20_utm:
    start = time.time()
    best_node, best_dist = nearest(root, t)
    end = time.time()
    nearest_results.append((best_node, best_dist))
    kd_times.append(end - start)
    print("BUSQUEDA CON KD-TREE")
    print("Coordenada:", t)
    print("Nodo más cercano:", best_node.point)
    print("Distancia:", best_dist, "m")
    print("Node ID:", best_node.node_id, "\n\n")


from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np



coords_array = np.array(coords_20_utm)
vor = Voronoi(coords_array)


fig, ax = plt.subplots(figsize=(10, 10))
voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='black', line_width=1)

#Graficar hospitales
ax.scatter(coords_array[:,0], coords_array[:,1], c='red', s=50, label="Hospitales")

#Etiquetas
for i, (x, y) in enumerate(coords_array):
    ax.text(x, y, f"H{i}", fontsize=9, color="darkred")

ax.set_title("Diagrama de Voronoi de Hospitales (UTM)")
ax.set_xlabel("X (metros)")
ax.set_ylabel("Y (metros)")
ax.legend()
ax.grid(True)

plt.show()


def punto_en_region(lat, lon):
    x, y = transformer.transform(lon, lat)
    punto = np.array([x, y])

    best_node, dist = nearest(root, (x, y))

    print("Hospital más cercano:", best_node.node_id)
    print("Distancia:", dist, "m")

    fig, ax = plt.subplots(figsize=(10, 10))
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='black')

    ax.scatter(coords_array[:,0], coords_array[:,1], c='red', s=50, label="Hospitales")

    ax.scatter([x], [y], c='blue', s=80, label="Punto del usuario")
    ax.text(x, y, " Usuario", color="blue", fontsize=10)

    ax.set_title("Punto del usuario sobre el diagrama de Voronoi")
    ax.legend()
    ax.grid(True)
    plt.show()


def region_voronoi(lat, lon):
    x, y = transformer.transform(lon, lat)
    punto = np.array([x, y])

    coords = np.array(coords_20_utm)
    dists = np.linalg.norm(coords - punto, axis=1)

    idx = dists.argmin()

   
    return idx, lista_de_hospitales[idx], dists[idx]

print("Por favor, ingresa tu ubicacion (latitud, longitud)")

lat = float(input("Latitud: "))
lon = float(input("Longitud: "))
punto_en_region(lat, lon)


idx, coordenadas, distancia = region_voronoi(lat,lon)

ux, uy = transformer.transform(lon, lat)
best_user_node, dist_user = nearest(root, (ux, uy))
print(f"Nodo de inicio (más cercano al punto solicitado): {best_user_node.node_id}")

best_hospital_node, dist_hosp = nearest_results[idx]
print(f"Nodo destino (hospital más cercano): {best_hospital_node.node_id}")
print(f"Distancia del hospital al nodo: {dist_hosp} m")



# coordenadas del nodo inicio
x1, y1 = best_user_node.point

# coordenadas del nodo destino
x2, y2 = best_hospital_node.point

distancia_nodos = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

print(f"\nDistancia entre nodo inicio y nodo destino: {distancia_nodos:.2f} m")

# info extra
print(f"\nHospital más cercano (idx): {idx}")
print(f"Coordenadas del hospital: {coordenadas}")
print(f"Distancia desde el usuario al hospital (UTM): {distancia:.2f} m")

import Astar
from simpleai.search import SearchProblem, astar

problem = Astar.OSMRouteProblem(G, best_user_node.node_id, best_hospital_node.node_id)

start = time.time()
result = astar(problem, graph_search=True)
end = time.time()

if result is None:
    print("A* no encontró ruta.")
else:
    ruta = [state for action, state in result.path()]
    print("\n Ruta A* usando SimpleAI:", ruta, " tiempo:", end-start, " segundos \n")
    ox.plot_graph_route(G, ruta, route_color='red', route_linewidth=3, node_size=0)