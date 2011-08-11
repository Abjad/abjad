from abjad.checks._Check import _Check
from abjad.tools.spannertools import HairpinSpanner


class ShortHairpinCheck(_Check):
    '''Hairpins must span at least two leaves.
    '''

    def _run(self, expr):
        from abjad.tools import spannertools
        violators = [ ]
        total, bad = 0, 0
        #hairpins = [
        #   p for p in expr.spanners.contained if isinstance(p, HairpinSpanner)]
        hairpins = spannertools.get_spanners_attached_to_any_improper_child_of_component(
            expr, HairpinSpanner)
        for hairpin in hairpins:
            if len(hairpin.leaves) <= 1:
                violators.append(hairpin)
            total += 1
        return violators, total
