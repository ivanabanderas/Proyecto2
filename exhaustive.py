# exhaustive.py
import math

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def exhaustive(points, node_ids, target):
    best_dist = float("inf")
    best_point = None
    best_id = None

    for p, nid in zip(points, node_ids):
        d = distance(target, p)
        if d < best_dist:
            best_dist = d
            best_point = p
            best_id = nid

    return best_point, best_dist, best_id
