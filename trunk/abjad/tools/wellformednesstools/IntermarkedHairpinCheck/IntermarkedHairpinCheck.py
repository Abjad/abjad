from abjad.tools import contexttools
from abjad.tools import spannertools
from abjad.tools import spannertools
from abjad.tools.wellformednesstools.Check import Check


class IntermarkedHairpinCheck(Check):
    '''Are there any dynamic marks in the middle of a hairpin?
    '''

    def _run(self, expr):
        violators = []
        total, bad = 0, 0
        spanner_classes = (spannertools.HairpinSpanner, )
        hairpins = \
            spannertools.get_spanners_attached_to_any_improper_child_of_component(
            expr, spanner_classes=spanner_classes)
        for hairpin in hairpins:
            if 2 < len(hairpin.leaves):
                for leaf in hairpin.leaves[1:-1]:
                    if leaf.get_marks(contexttools.DynamicMark):
                        violators.append(hairpin)
                        bad += 1
                        break
            total += 1
        return violators, total
