
#---------------
# Componente 2
#---------------

import BFS 
import DFS
import UCS    
import Astar
import IDDFS
import time
import osmnx as ox
from simpleai.search import SearchProblem, astar
from grafo import graph
from puntosRandom import pares_nodos_por_distancia


G, points, node_ids = graph("Av. Mariano Otero 3000, Jardines del Sol, 45050 Zapopan, Jal.", dist=10000)

G_proj = ox.project_graph(G)

# metas


# ----------------------------------------------------------
#  BFS
# ----------------------------------------------------------
start = time.time()
caminoBFS = BFS.BFSMain(G_proj, metas[0]["nodo_1"], metas[0]["nodo_2"])
end = time.time()

if caminoBFS:
    print("\n Camino BFS:", caminoBFS, " tiempo: ", end - start, " segundos \n")
    ox.plot_graph_route(G_proj, caminoBFS, route_color='r', route_linewidth=3, node_size=0)
else:
    print("No existe un camino posible para estos dos vértices.")


# ----------------------------------------------------------
#  DFS
# ----------------------------------------------------------
start = time.time()
caminoDFS = DFS.DFS(G_proj, metas[1]["nodo_1"], metas[1]["nodo_2"])
end = time.time()

if caminoDFS:
    print("\n Camino DFS:", caminoDFS, " tiempo: ", end - start, " segundos \n \n")
    ox.plot_graph_route(G_proj, caminoDFS, route_color='r', route_linewidth=3, node_size=0)
else:
    print("No existe camino.")


# ----------------------------------------------------------
#  UCS
# ----------------------------------------------------------
start = time.time()
ruta, costo = UCS.UCS(G_proj, metas[2]["nodo_1"], metas[2]["nodo_2"])
end = time.time()

if ruta:
    print("\n Camino UCS:", ruta, " costo:", costo, " tiempo:", end - start, " segundos \n")
    ox.plot_graph_route(G_proj, ruta, route_color='r', route_linewidth=3, node_size=0)
else:
    print("No existe camino.")


# ----------------------------------------------------------
#  A*
# ----------------------------------------------------------

problem = Astar.OSMRouteProblem(G_proj, metas[3]["nodo_1"], metas[3]["nodo_2"])

start = time.time()
result = astar(problem, graph_search=True)
end = time.time()

if result is None:
    print("A* no encontró ruta.")
else:
    ruta = [state for action, state in result.path()]
    print("Ruta A* usando SimpleAI:", ruta, " tiempo:", end-start, " segundos")
    ox.plot_graph_route(G_proj, ruta, route_color='red', route_linewidth=3, node_size=0)

# ----------------------------------------------------------
#  IDDFS  (CORRECCIÓN PRINCIPAL AQUÍ)
# ----------------------------------------------------------

problem = IDDFS.OSMRouteProblem(G_proj, metas[4]["nodo_1"], metas[4]["nodo_2"])

start = time.time()
ruta = IDDFS.iterative_deepening_search(problem, max_depth=150)
end = time.time()

if ruta:
    
    ruta_iddfs = ruta
    print(" \n Ruta IDDFS:", ruta_iddfs, " tiempo:", end - start, " segundos \n")
    ox.plot_graph_route(G_proj, ruta_iddfs, route_color='red', route_linewidth=3, node_size=0)
else:
    print("No existe camino (o profundidad insuficiente).")
