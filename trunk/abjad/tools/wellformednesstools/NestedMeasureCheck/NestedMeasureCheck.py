from abjad.tools import componenttools
from abjad.tools import measuretools
from abjad.tools.wellformednesstools.Check import Check


class NestedMeasureCheck(Check):
    '''Do we have any nested measures?'''

    def _run(self, expr):
        violators = []
        total = 0
        for t in measuretools.iterate_measures_forward_in_expr(expr):
            if componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(t, measuretools.Measure):
                violators.append(t)
            total += 1
        return violators, total
