from abjad.tools.wellformednesstools.Check import Check


class EmptyContainerCheck(Check):

    runtime = 'composition'

    def _run(self, expr):
        from abjad.tools import componenttools
        from abjad.tools.containertools.Container import Container
        violators = [ ]
        bad, total = 0, 0
        for t in componenttools.iterate_components_forward_in_expr(expr, Container):
            if len(t) == 0:
                violators.append(t)
                bad += 1
            total += 1
        return violators, total
