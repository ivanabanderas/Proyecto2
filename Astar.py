from simpleai.search import SearchProblem
import math

def heuristic_distance(G, a, b):
    x1, y1 = G.nodes[a]['x'], G.nodes[a]['y']
    x2, y2 = G.nodes[b]['x'], G.nodes[b]['y']
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


class OSMRouteProblem(SearchProblem):

    def __init__(self, graph, start, goal):
        self.G = graph
        self.goal = goal
        super().__init__(start)

    def actions(self, state):
        return list(self.G[state].keys())

    def result(self, state, action):
        return action

    def cost(self, state1, action, state2):
        edge_data = self.G[state1][state2][0]
        return edge_data.get('length', 1)

    def heuristic(self, state):
        return heuristic_distance(self.G, state, self.goal)

    def is_goal(self, state):
        return state == self.goal


