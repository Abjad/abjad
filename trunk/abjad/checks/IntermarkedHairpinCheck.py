from abjad.checks._Check import _Check
from abjad.tools.spannertools import HairpinSpanner


class IntermarkedHairpinCheck(_Check):
    '''Are there any dynamic marks in the middle of a hairpin?
    '''

    def _run(self, expr):
        from abjad.tools import contexttools
        from abjad.tools import spannertools
        violators = [ ]
        total, bad = 0, 0
        hairpins = spannertools.get_spanners_attached_to_any_improper_child_of_component(
            expr, HairpinSpanner)
        for hairpin in hairpins:
            if 2 < len(hairpin.leaves):
                for leaf in hairpin.leaves[1:-1]:
                    if contexttools.get_dynamic_marks_attached_to_component(leaf):
                        violators.append(hairpin)
                        bad += 1
                        break
            total += 1
        return violators, total
