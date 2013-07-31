from abjad.tools import iterationtools
from abjad.tools import selectiontools
from abjad.tools.wellformednesstools.Check import Check


class MissingParentCheck(Check):
    r'''Each node except the root needs a parent.
    '''

    def _run(self, expr):
        violators = []
        total = 0
        components = iterationtools.iterate_components_in_expr(expr)
        for i, component in enumerate(components):
            #total += 1
            #if component is not expr:
            if 0 < i:
                if component.parent is None:
                    violators.append(component)
        total = i + 1
        return violators, total
