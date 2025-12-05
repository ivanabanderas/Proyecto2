
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
from puntosRandom import obtener_5_parejas




G, points, node_ids = graph("Av. Mariano Otero 3000, Jardines del Sol, 45050 Zapopan, Jal.", dist=10000)


# metas
metas = obtener_5_parejas(G, dist_min=100,dist_max=500) #regresa una lista de 5 pares de puntos y verifica el rango entre ellos 1er caso (maximo 1000 metros)
# metas = obtener_5_parejas(G, dist_min=1000,dist_max=5000) #regresa una lista de 5 pares de puntos y verifica el rango entre ellos 2ndo caso (de 1000 a 5000 metros)
# metas = obtener_5_parejas(G, dist_min=5000,dist_max=10000) #regresa una lista de 5 pares de puntos y verifica el rango entre ellos 1er caso (desde 5000 o más metros, (maximo llega a 10000 porque es el limite establecido en el plano))


# ----------------------------------------------------------
#  BFS
# ----------------------------------------------------------
for origen, destino in metas:
    start = time.time()
    camino = BFS.BFSMain(G, origen, destino)
    end = time.time()

    print(f"\nVertice de inicio: {origen} Verice objetivo {destino} (destinos escogidos aleatoriamente) \n")
    if camino:
        print("Camino BFS:", camino, "Tiempo:", end - start, "segundos")
        ox.plot_graph_route(G, camino, route_color='r', route_linewidth=3, node_size=0)
    else:
        print("No existe camino BFS.")

# ----------------------------------------------------------
#  DFS
# ----------------------------------------------------------
for origen, destino in metas:
    start = time.time()
    camino = DFS.DFS(G, origen, destino)
    end = time.time()

    print(f"\nVertice de inicio: {origen} Verice objetivo {destino} (destinos escogidos aleatoriamente)")
    if camino:
        print("\n Camino ahora con DFS:", camino, "Tiempo:", end - start, "segundos \n")
        ox.plot_graph_route(G, camino, route_color='r', route_linewidth=3, node_size=0)
    else:
        print("No existe camino BFS.")


# ----------------------------------------------------------
#  UCS
# ----------------------------------------------------------

for origen, destino in metas:
    start = time.time()
    ruta, costo = UCS.UCS(G, origen, destino)
    end = time.time()

    if ruta:
        print("\n Camino UCS:", ruta, " costo:", costo, " tiempo:", end - start, " segundos \n")
        ox.plot_graph_route(G, ruta, route_color='r', route_linewidth=3, node_size=0)
    else:
        print("No existe camino.")


# ----------------------------------------------------------
#  A*
# ----------------------------------------------------------


for origen, destino in metas:
    
    problem = Astar.OSMRouteProblem(G, origen, destino)

    start = time.time()
    result = astar(problem, graph_search=True)
    end = time.time()

    if result is None:
        print("A* no encontró ruta.")
    else:
        ruta = [state for action, state in result.path()]
        print("\n Ruta A* usando SimpleAI:", ruta, " tiempo:", end-start, " segundos \n")
        ox.plot_graph_route(G, ruta, route_color='red', route_linewidth=3, node_size=0)

# # ----------------------------------------------------------
#  IDDFS 
# ----------------------------------------------------------


for origen,destino in metas:
    problem = IDDFS.OSMRouteProblem(G, origen, destino)

    start = time.time()
    ruta = IDDFS.iterative_deepening_search(problem, max_depth=150)
    end = time.time()

    if ruta:
        
        ruta_iddfs = ruta
        print(" \n Ruta IDDFS:", ruta_iddfs, " tiempo:", end - start, " segundos \n")
        ox.plot_graph_route(G, ruta_iddfs, route_color='red', route_linewidth=3, node_size=0)
    else:
        print("No existe camino (o profundidad insuficiente).")
