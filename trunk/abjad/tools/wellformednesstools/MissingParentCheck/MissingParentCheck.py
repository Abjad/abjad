from abjad.tools import iterationtools
from abjad.tools.wellformednesstools.Check import Check


class MissingParentCheck(Check):
    '''Each node except the root needs a parent.
    '''

    def _run(self, expr):
        violators = []
        total = 0
        for component in iterationtools.iterate_components_in_expr(expr):
            total += 1
            if component is not expr:
                if component.parent is None:
                    violators.append(component)
        return violators, total
