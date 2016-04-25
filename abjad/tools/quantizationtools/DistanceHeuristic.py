# -*- coding: utf-8 -*-
from abjad.tools.quantizationtools.Heuristic import Heuristic


class DistanceHeuristic(Heuristic):
    r'''Concrete ``Heuristic`` subclass which considers only the
    computed distance of each ``QGrid`` and the number of leaves of
    that ``QGrid`` when choosing the optimal ``QGrid`` for a given
    ``QTargetBeat``.

    The ``QGrid`` with the smallest distance and fewest number of
    leaves will be selected.

    Return ``DistanceHeuristic`` instance.
    '''

    ### PRIVATE METHODS ###

    def _process(self, q_target_beats):
        from abjad.tools import quantizationtools
        for q_target_beat in q_target_beats:
            q_grids = q_target_beat.q_grids
            if q_grids:
                sorted_q_grids = sorted(
                    q_grids, key=lambda x: (x.distance, len(x.leaves)))
                q_target_beat._q_grid = sorted_q_grids[0]
            else:
                q_target_beat._q_grid = quantizationtools.QGrid()
        return q_target_beats
