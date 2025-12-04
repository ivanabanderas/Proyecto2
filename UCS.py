from queue import PriorityQueue
import osmnx as ox

def UCS(G, start, goal):

    frontier = PriorityQueue()
    frontier.put((0, start))
    
    dist = {start: 0}
    parents = {start: None}

    explored = set()

    while not frontier.empty():

        cost, current = frontier.get()

        # Si el nodo ya fue expandido antes con menor costo → ignorar
        if current in explored:
            continue
        
        explored.add(current)

        # Si ya llegamos
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parents[current]
            return list(reversed(path)), cost

        # Explorar vecinos
        for neighbor in G[current]:

            # costo de arista
            edge_data = list(G[current][neighbor].values())[0]
            weight = edge_data.get("length", 1)

            new_cost = cost + weight

            # Si es un nuevo nodo o encontramos mejor costo
            if neighbor not in dist or new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                parents[neighbor] = current
                frontier.put((new_cost, neighbor))

    return None, None



