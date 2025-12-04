from queue import LifoQueue
import osmnx as ox


def DFS(G, start, goal):

    frontier = LifoQueue() 
    frontier.put(start)

    explored = {node: False for node in G.nodes()}
    explored[start] = True

    parents = {start: None}

    while True:
        
        if frontier.empty():
            return None
        
        current = frontier.get()

        # Si ya llegamos al destino
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parents[current]
            return list(reversed(path))

        # Explorar vecinos del nodo actual
        for neighbor in G[current]:
            if not explored[neighbor]:
                frontier.put(neighbor)
                explored[neighbor] = True
                parents[neighbor] = current
