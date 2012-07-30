from experimental.quantizationtools.Heuristic import Heuristic


class DistanceHeuristic(Heuristic):

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, list_of_list_of_q_grids):
        result = []
        for list_of_q_grids in list_of_list_of_q_grids:
            sorted_q_grids = sorted(list_of_q_grids, key=lambda x: (x.distance, len(x.leaves)))
            result.append(sorted_q_grids[0])
        return result
