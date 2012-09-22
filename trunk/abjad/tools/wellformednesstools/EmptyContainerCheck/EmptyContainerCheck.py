from abjad.tools import containertools
from abjad.tools import iterationtools
from abjad.tools.wellformednesstools.Check import Check


class EmptyContainerCheck(Check):

    runtime = 'composition'

    def _run(self, expr):
        violators = []
        bad, total = 0, 0
        for t in iterationtools.iterate_components_in_expr(expr, containertools.Container):
            if len(t) == 0:
                violators.append(t)
                bad += 1
            total += 1
        return violators, total
