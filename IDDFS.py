
from simpleai.search import SearchProblem
import osmnx as ox

class OSMRouteProblem(SearchProblem):

    def __init__(self, graph, start, goal):
        self.G = graph
        self.goal = goal
        super().__init__(start)

    def actions(self, state):
        return list(self.G[state].keys())

    def result(self, state, action):
        return action

    def is_goal(self, state):
        return state == self.goal



def depth_limited_search(problem, limit):

    def recursive_dls(state, parent, depth):
        if problem.is_goal(state):
            return [state]

        if depth == limit:
            return None

        for action in problem.actions(state):
            next_state = problem.result(state, action)
            if next_state != parent:    
                result = recursive_dls(next_state, state, depth + 1)
                if result is not None:
                    return [state] + result

        return None

    return recursive_dls(problem.initial_state, None, 0)



def iterative_deepening_search(problem, max_depth=50):
    for depth in range(max_depth + 1):
        result = depth_limited_search(problem, depth)
        if result is not None:
            return result
    return None



