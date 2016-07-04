# -*- coding: utf-8 -*-
from abjad.tools import metertools
from abjad.tools import scoretools
from abjad.tools.topleveltools import mutate
from abjad.tools.quantizationtools.AttackPointOptimizer \
    import AttackPointOptimizer


class MeasurewiseAttackPointOptimizer(AttackPointOptimizer):
    r'''Concrete ``AttackPointOptimizer`` instance which attempts to optimize
    attack points in an expression with regard to the effective time signature
    of that expression.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> show(staff) # doctest: +SKIP

    ::

        >>> source_tempo = Tempo((1, 4), 60)
        >>> q_events = quantizationtools.QEventSequence.from_tempo_scaled_leaves(
        ...     staff[:],
        ...     tempo=source_tempo,
        ...     )
        >>> target_tempo = Tempo((1, 4), 54)
        >>> q_schema = quantizationtools.MeasurewiseQSchema(
        ...     tempo=target_tempo,
        ...     )
        >>> quantizer = quantizationtools.Quantizer()

    Without the measure-wise attack-point optimizer:

    ::

        >>> result = quantizer(
        ...     q_events,
        ...     q_schema=q_schema,
        ...     )
        >>> show(result) # doctest: +SKIP

    With the measure-wise attack-point optimizer:

    ::

        >>> optimizer = quantizationtools.MeasurewiseAttackPointOptimizer()
        >>> result = quantizer(
        ...     q_events,
        ...     attack_point_optimizer=optimizer,
        ...     q_schema=q_schema,
        ...     )
        >>> show(result) # doctest: +SKIP

    Only acts on Measure instances.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls measurewise attack-point optimizer.

        Returns none.
        '''
        assert isinstance(expr, scoretools.Measure)
        meter = metertools.Meter(expr)
        mutate(expr[:]).rewrite_meter(
            meter,
            boundary_depth=1,
            )