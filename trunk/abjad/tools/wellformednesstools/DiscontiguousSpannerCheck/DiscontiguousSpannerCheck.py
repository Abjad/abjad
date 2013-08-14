# -*- encoding: utf-8 -*-
from abjad.tools import componenttools
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools.wellformednesstools.Check import Check
Selection = selectiontools.Selection


class DiscontiguousSpannerCheck(Check):
    r'''There are now two different types of spanner.
    Most spanners demand that spanner components be logical-voice-contiguous.
    But a few special spanners (like Tempo) do not make such a demand.
    The check here consults the experimental `_contiguity_constraint`.
    '''

    def _run(self, expr):
        violators = []
        total, bad = 0, 0
        for spanner in \
            spannertools.get_spanners_attached_to_any_improper_child_of_component(
            expr):
            if spanner._contiguity_constraint == 'logical voice':
                if not Selection._all_are_contiguous_components_in_same_logical_voice(
                    spanner[:]):
                    violators.append(spanner)
            total += 1
        return violators, total
