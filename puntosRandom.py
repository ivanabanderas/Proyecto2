import osmnx as ox
import random
import numpy as np
from kdTree import build_kd_tree, KDNode


def dist(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2) ** 0.5


def buscar_radio(node, target, radius, results):
    if node is None:
        return

    axis = node.axis
    value = node.value

    # Si es hoja
    if node.point is not None:
        if dist(target, node.point) <= radius:
            results.append((node.node_id, node.point))
        return

    # Buscar en ramas relevantes
    if target[axis] - radius <= value:
        buscar_radio(node.left, target, radius, results)

    if target[axis] + radius >= value:
        buscar_radio(node.right, target, radius, results)


# --------------------------------------------------------
# Obtener 5 parejas dentro de un rango de distancias
# dist_min ≤ distancia ≤ dist_max
# --------------------------------------------------------
def obtener_5_parejas(G_proj, dist_min=0, dist_max=1000):

    # Obtener puntos e IDs
    points = []
    node_ids = []

    for nid, data in G_proj.nodes(data=True):
        points.append((data['x'], data['y']))  # coordenadas proyectadas
        node_ids.append(nid)

    # Construir KD-tree
    root = build_kd_tree(points, node_ids)

    # Map para obtener coordenadas rápidas
    id_to_point = {nid: p for nid, p in zip(node_ids, points)}

    parejas = []
    nodos_usados = set()     # para garantizar nodos diferentes en cada pareja

    print("Buscando parejas dentro del rango:", dist_min, "a", dist_max, "metros...")

    # Iteramos en orden aleatorio para obtener variedad
    random.shuffle(node_ids)

    for nid in node_ids:

        # Si ya está usado, lo saltamos
        if nid in nodos_usados:
            continue

        p = id_to_point[nid]

        # Buscar candidatos dentro del radio máximo
        encontrados = []
        buscar_radio(root, p, dist_max, encontrados)

        # Filtrar por rango mínimo y nodos no usados
        candidatos = [(vid, pt) for vid, pt in encontrados
                      if vid != nid
                      and vid not in nodos_usados
                      and dist_min <= dist(p, pt) <= dist_max]

        if not candidatos:
            continue

        # Elegimos 1 vecino para emparejar
        vecino_id, _ = random.choice(candidatos)

        parejas.append((nid, vecino_id))
        nodos_usados.add(nid)
        nodos_usados.add(vecino_id)

        if len(parejas) == 5:
            return parejas

    return parejas


# --------------------------------------------------------
# Ejemplo de uso
# --------------------------------------------------------
direccion = "Av. Mariano Otero 3000, Jardines del Sol, 45050 Zapopan, Jal."
G = ox.graph_from_address(direccion, dist=10000, network_type='drive')
G_proj = ox.project_graph(G)


pares = obtener_5_parejas(
    G_proj,
    dist_min=100,      # mínimo en metros
    dist_max=1000      # máximo en metros
)

print(pares)
