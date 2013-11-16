# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools.quantizationtools.AttackPointOptimizer \
	import AttackPointOptimizer


class MeasurewiseAttackPointOptimizer(AttackPointOptimizer):
    r'''Concrete ``AttackPointOptimizer`` instance which attempts to optimize
    attack points in an expression with regard to the effective time 
    signature of that expression.

    Only acts on Measure instances.

    Return ``MeasurewiseAttackPointOptimizer`` instance.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        from abjad.tools import quantizationtools
        assert isinstance(expr, scoretools.Measure)
        meter = metertools.Meter(expr)
        metertools.rewrite_meter(
            expr[:], meter)
