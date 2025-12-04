
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


G, points, node_ids = graph("Av. Mariano Otero 3000, Jardines del Sol, 45050 Zapopan, Jal.", dist=10000)

G_proj = ox.project_graph(G)

# metas
metas = [
    [4758713730, 1780012311],
    [1975947235, 1609786704],
    [1796560746, 1796560732],
    [1380714005, 6135370558],
    [1368257237, 631800880]
]


# ----------------------------------------------------------
#  BFS
# ----------------------------------------------------------
start = time.time()
caminoBFS = BFS.BFSMain(G_proj, metas[0][0], metas[0][1])
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
caminoDFS = DFS.DFS(G_proj, metas[1][0], metas[1][1])
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
ruta, costo = UCS.UCS(G_proj, metas[2][0], metas[2][1])
end = time.time()

if ruta:
    print("\n Camino UCS:", ruta, " costo:", costo, " tiempo:", end - start, " segundos \n")
    ox.plot_graph_route(G_proj, ruta, route_color='r', route_linewidth=3, node_size=0)
else:
    print("No existe camino.")


# ----------------------------------------------------------
#  A*
# ----------------------------------------------------------

problem = Astar.OSMRouteProblem(G_proj, metas[3][0], metas[3][1])

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

problem = IDDFS.OSMRouteProblem(G_proj, metas[4][0], metas[4][1])

start = time.time()
ruta = IDDFS.iterative_deepening_search(problem, max_depth=150)
end = time.time()

if ruta:
    
    ruta_iddfs = ruta
    print(" \n Ruta IDDFS:", ruta_iddfs, " tiempo:", end - start, " segundos \n")
    ox.plot_graph_route(G_proj, ruta_iddfs, route_color='red', route_linewidth=3, node_size=0)
else:
    print("No existe camino (o profundidad insuficiente).")
