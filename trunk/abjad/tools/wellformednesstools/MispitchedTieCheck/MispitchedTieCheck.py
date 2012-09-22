from abjad.tools import iterationtools
from abjad.tools import leaftools
from abjad.tools import notetools
from abjad.tools import spannertools
from abjad.tools import tietools
from abjad.tools.wellformednesstools.Check import Check


class MispitchedTieCheck(Check):

    def _run(self, expr):
        '''Check for mispitched notes.
        Do not check tied rests or skips.
        Implement chord-checking later.
        '''
        violators = []
        total = 0
        for leaf in iterationtools.iterate_components_in_expr(expr, notetools.Note):
            total += 1
            spanners = spannertools.get_spanners_attached_to_component(
                leaf, tietools.TieSpanner)
            if spanners:
                spanner = spanners.pop()
                if not spanner._is_my_last_leaf(leaf):
                    next_leaf = leaftools.get_nth_leaf_in_thread_from_leaf(leaf, 1)
                    if next_leaf:
                        if leaf.written_pitch != next_leaf.written_pitch:
                            violators.append(leaf)
        return violators, total
