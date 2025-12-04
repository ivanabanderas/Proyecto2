#pip install osmnx 
import osmnx as ox
import numpy as np

def graph(address, dist, network_type='drive'):

    G = ox.graph_from_address(address, dist=dist, network_type=network_type)
    G_proj = ox.project_graph(G)

    coords = []
    node_ids = []

    for node, data in G_proj.nodes(data=True):
        x = data['x']
        y = data['y']
        coords.append((x, y))
        node_ids.append(node)

    points = np.array(coords)

    return G_proj, points, node_ids