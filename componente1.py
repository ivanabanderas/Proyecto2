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

coords_20 = [
    (20.6530146, -103.3950168), #expo guadalajara    1
    (20.6495422, -103.4025252),    #plaza del Sol    2
    (20.645692, -103.404553),   #Teatro Galerías  3
    (20.6662872, -103.4027127),   #Glorieta chapalita 4
    (20.66277938304262, -103.4048075594733),    #El Terrible Juan Chapalita  5
    (20.668873011303333, -103.40497928797325), #El Sotano    6
    (20.674645179414604, -103.38744501769607),   #La Minerva 7
    (20.660840308435066, -103.41838488771572),   #UNIVA  8
    (20.67794548616333, -103.4322036280186),   #Plaza Galerias   9
    (20.666614043686543, -103.39341167098077),   #RIU    10
    (20.669057091070474, -103.40521925871414),   #Anahuacali 11
    (20.667003894225147, -103.4099179911167),  #Walmart niño obrero  12
    (20.676995086672317, -103.41405028466093),  #Hard Rock Cafe  13
    (20.675072120242135, -103.39296332760927),   #Plaza Sania    14
    (20.65676194297229, -103.38243084460854),   #Mercado de abastos  15
    (20.674503315328426, -103.38070481742233),   #Centro Magno   16
    (20.679248076617146, -103.42829067462256),  #Costco  17
    (20.65552543688159, -103.4064799133188),   #Plaza Xochitl    18
    (20.657011226197397, -103.39905555869316),   #IKEA   19
    (20.678731846183553, -103.39433192774229)   #Galeria del Calzado    20
]

transformer = Transformer.from_crs(4326, 32613, always_xy=True)

coords_20_utm = []
for lat, lon in coords_20:
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


exhaustive_results = []
exh_times = []

for t in coords_20_utm:
    start = time.time()
    best_point, best_dist, best_id = exhaustive(points, node_ids, t)
    end = time.time()
    exhaustive_results.append((best_point, best_dist))
    exh_times.append(end - start)
    print("BUSQUEDA EXHAUSTIVA")
    print("Coordenada:", t)
    print("Nodo más cercano", best_point)
    print("Distancia:", best_dist, "m")
    print("Node ID:", best_id, "\n\n")

#Visualizacion componente 1

fig = plt.figure(figsize=(15, 8))
gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])  
ax_map = fig.add_subplot(gs[0])
ox.plot_graph( 
    G, 
    ax=ax_map,
    show=False, 
    close=False, 
    node_size=0,        # nodos del grafo invisibles
    edge_color='lightgray', 
    edge_linewidth=0.5
)
# extraemos x, y
x_coords = [p[0] for p in coords_20_utm]
y_coords = [p[1] for p in coords_20_utm]

ax_map.scatter(x_coords, y_coords, c='red', s=50, label='Coordenadas objetivo')

ax_map.text(
    0.02, 0.98,
    f"Tiempo de construcción KD-tree:\n{round(kdTree_time, 4)} s",
    transform=ax_map.transAxes,
    fontsize=10,
    verticalalignment='top',
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7)
)

# Extraemos coordenadas X e Y
nearest_x = [n.point[0] for n, _ in nearest_results]
nearest_y = [n.point[1] for n, _ in nearest_results]
ax_map.scatter(nearest_x, nearest_y, c='blue', s=50, label='Nodo más cercano (KD-tree)')
ax_map.legend()
plt.pause(3)            # Esperar 3 segundos


# Extraemos X e Y
exhaustive_x = [p[0] for p, _ in exhaustive_results]
exhaustive_y = [p[1] for p, _  in exhaustive_results]
ax_map.scatter(exhaustive_x, exhaustive_y, c='green', s=50, label='Nodo más cercano (Busqueda exhaustiva)')

ax_map.legend()


ax_table = fig.add_subplot(gs[1])
ax_table.axis('off')  # ocultamos ejes para la tabla

col_labels = ["Coordenada", "KD-tree (s)", "Exhaustiva (s)"]
table_data = [[i+1, round(kd_times[i],5), round(exh_times[i],5)] for i in range(len(coords_20_utm))]
table = ax_table.table(cellText=table_data, colLabels=col_labels, loc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.5)

plt.show()