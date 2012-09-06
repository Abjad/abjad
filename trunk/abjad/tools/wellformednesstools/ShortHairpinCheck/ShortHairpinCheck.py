from abjad.tools import spannertools
from abjad.tools.wellformednesstools.Check import Check


class ShortHairpinCheck(Check):
    '''Hairpins must span at least two leaves.
    '''

    def _run(self, expr):
        violators = []
        total, bad = 0, 0
        #hairpins = [
        #   p for p in expr.spanners.contained if isinstance(p, HairpinSpanner)]
        hairpins = spannertools.get_spanners_attached_to_any_improper_child_of_component(
            expr, spannertools.HairpinSpanner)
        for hairpin in hairpins:
            if len(hairpin.leaves) <= 1:
                violators.append(hairpin)
            total += 1
        return violators, total
