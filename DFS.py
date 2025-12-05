from queue import LifoQueue
import time
import osmnx as ox


def DFS(G, v_inicio, v_final):

    frontier = LifoQueue() 
    frontier.put(v_inicio)

    explored = {node: False for node in G.nodes()}
    explored[v_inicio] = True

    parents = {v_inicio: None}

    while True:
        
        if frontier.empty():
            return None
        
        current = frontier.get()

        if current == v_final:
            path = []
            while current is not None:
                path.append(current)
                current = parents[current]
            return list(reversed(path))

        for neighbor in G[current]:
            if not explored[neighbor]:
                frontier.put(neighbor)
                explored[neighbor] = True
                parents[neighbor] = current


