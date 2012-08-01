from experimental.quantizationtools.Heuristic import Heuristic


class DistanceHeuristic(Heuristic):

    ### PRIVATE METHODS ###

    def _process(self, q_target_beats):
        for q_target_beat in q_target_beats:
            q_grids = q_target_beat.q_grids
            sorted_q_grids = sorted(q_grids, key=lambda x: (x.distance, len(x.leaves)))
            q_target_beat._q_grid = sorted_q_grids[0]
        return q_target_beats
