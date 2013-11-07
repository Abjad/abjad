# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.functiontools import iterate
from abjad.tools.wellformednesstools.Check import Check


class EmptyContainerCheck(Check):

    runtime = 'composition'

    def _run(self, expr):
        violators = []
        bad, total = 0, 0
        for component in iterate(expr).by_class(scoretools.Container):
            if len(component) == 0:
                violators.append(component)
                bad += 1
            total += 1
        return violators, total
