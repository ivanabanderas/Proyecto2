from grafo import graph
import time
import osmnx as ox
import random
from kdTree import build_kd_tree, nearest

G, points, node_ids = graph("Av. Mariano Otero 3000, Jardines del Sol, 45050 Zapopan, Jal.", dist=10000)
#ox.plot_graph(G)

print("\nConstruyendo KD-tree...")
start = time.time()
root = build_kd_tree(points.tolist(), node_ids, depth=0)
end = time.time()

print(f"KD-tree construido en {end - start:.4f} segundos")

import random
sample = random.sample(list(points), 20)
for t in sample:
    best_node, best_dist = nearest(root, t)