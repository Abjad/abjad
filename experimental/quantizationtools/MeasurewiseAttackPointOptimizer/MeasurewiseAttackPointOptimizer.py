from abjad.tools import contexttools
from abjad.tools import measuretools
from abjad.tools import tuplettools
from experimental.quantizationtools.AttackPointOptimizer import AttackPointOptimizer


class MeasurewiseAttackPointOptimizer(AttackPointOptimizer):
    '''The MeasurewiseAttackPointOptimizer attempts to optimize attack points
    in an expression with regard for the effective time signature of that
    expression.

    It only acts on Measure instances.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        from experimental import quantizationtools

        assert isinstance(expr, measuretools.Measure)

        if len(expr) == 1 and isinstance(expr[0], tuplettools.Tuplet):
            quantizationtools.NaiveAttackPointOptimizer()(expr.leaves)
            return

        time_signature = contexttools.get_effective_time_signature(expr)

        beat_hierarchy = quantizationtools.BeatHierarchy(time_signature)
