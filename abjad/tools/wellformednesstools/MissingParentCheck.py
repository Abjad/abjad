# -*- encoding: utf-8 -*-
from abjad.tools.functiontools import iterate
from abjad.tools.wellformednesstools.Check import Check


class MissingParentCheck(Check):
    r'''Each node except the root needs a parent.
    '''

    def _run(self, expr):
        violators = []
        total = 0
        components = iterate(expr).by_class()
        for i, component in enumerate(components):
            #total += 1
            #if component is not expr:
            if 0 < i:
                if component._parent is None:
                    violators.append(component)
        total = i + 1
        return violators, total
