from grafo import graph
import math 
import time 

class KDNode:
    def __init__(self, point=None, node_id=None, axis=None, value=None, left=None, right=None):  
        self.point = point          # (x, y)
        self.node_id = node_id      # ID real
        self.axis = axis            # 0 = x, 1 = y
        self.value = value
        self.left = left            # subárbol izquierdo
        self.right = right          # subárbol derecho

def build_kd_tree(points, node_ids, depth=0):
    if len(points) == 1:
        return KDNode(
            point=points[0], 
            node_id = node_ids[0], 
            axis=depth%2
        )

    axis = depth % 2

    # Ordenar por el eje correspondiente
    sorted_data = sorted(zip(points, node_ids), key=lambda x: x[0][axis])
    points_final = [p for p, _ in sorted_data]
    ids_final = [n for _, n in sorted_data]

    n = len(points_final)

    if n%2 == 1:
        median_value = points_final[n//2][axis]
    else:
        median_value = ((points_final[n//2 - 1][axis]) + (points_final[n//2][axis]))/2

    points_left = []
    points_right = []
    left_ids = []
    right_ids = []

    for p, nid in zip(points_final, ids_final):
        if p[axis] <= median_value:
            points_left.append(p)
            left_ids.append(nid)
        else:
            points_right.append(p)
            right_ids.append(nid)


    v_left = build_kd_tree(points_left, left_ids, depth + 1)
    v_right = build_kd_tree(points_right, right_ids, depth + 1)

    v = KDNode(
        axis = axis,
        value = median_value,
        left = v_left,
        right = v_right
        )

    return v

def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def nearest(node, target, best_node = None, best_distance = float("inf")):

    if node is None:
        return best_node.point, best_distance
    
    if node.point is not None:
        dist = distance(target, node.point)
        if dist < best_distance:
            best_node = node
            best_distance = dist
        return best_node, best_distance
    
    axis = node.axis
    diff = target[axis] - node.value

    if diff <= 0:
        near = node.left
        far = node.right 
    else:
        near = node.right
        far = node.left 

    best_node, best_distance = nearest(near, target,best_node, best_distance)

    if abs(diff) < best_distance:
        best_node, best_distance = nearest(far, target,best_node, best_distance)

    return best_node, best_distance