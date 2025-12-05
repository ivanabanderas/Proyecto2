from queue import PriorityQueue
import osmnx as ox

def UCS(G, v_inicio, v_final):

    frontier = PriorityQueue()
    frontier.put((0, v_inicio))
    
    dist = {v_inicio: 0}
    parents = {v_inicio: None}

    explored = set()

    while not frontier.empty():

        cost, current = frontier.get()

        if current in explored:
            continue
        
        explored.add(current)

        if current == v_final:
            path = []
            while current is not None:
                path.append(current)
                current = parents[current]
            return list(reversed(path)), cost

        for neighbor in G[current]:

            edge_data = list(G[current][neighbor].values())[0]
            weight = edge_data.get("length", 1)

            new_cost = cost + weight

            if neighbor not in dist or new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                parents[neighbor] = current
                frontier.put((new_cost, neighbor))

    return None, None



