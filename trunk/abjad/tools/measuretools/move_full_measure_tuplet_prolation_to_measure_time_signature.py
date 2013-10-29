# -*- encoding: utf-8 -*-
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import mutationtools


def move_full_measure_tuplet_prolation_to_measure_time_signature(expr):
    r'''Move prolation of full-measure tuplet to time signature of measure.

    Measures usually become non-power-of-two as as result:

    ::

        >>> t = Measure((2, 8), [tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")])
        >>> measuretools.move_full_measure_tuplet_prolation_to_measure_time_signature(t)

    ..  doctest::

        >>> f(t)
        {
            \time 3/12
            \scaleDurations #'(2 . 3) {
                c'8
                d'8
                e'8
            }
        }

    Returns none.
    '''
    from abjad.tools import scoretools
    from abjad.tools import contexttools
    from abjad.tools import iterationtools
    from abjad.tools import tuplettools
    from abjad.tools.scoretools import attach

    for measure in iterationtools.iterate_measures_in_expr(expr):
        if len(measure) == 1:
            if isinstance(measure[0], tuplettools.Tuplet):
                tuplet = measure[0]
                tuplet_multiplier = tuplet.multiplier
                tuplet_denominator = tuplet_multiplier.denominator
                reduced_denominator = mathtools.remove_powers_of_two(tuplet_denominator)
                time_signature = measure.time_signature
                time_signature_rational = durationtools.Duration(
                    time_signature.numerator, time_signature.denominator)
                numerator = time_signature_rational.numerator * reduced_denominator
                denominator = time_signature_rational.denominator * reduced_denominator
                time_signature = contexttools.TimeSignatureMark((numerator, denominator))
                for mark in measure._get_marks(contexttools.TimeSignatureMark):
                    mark.detach()
                attach(time_signature, measure)
                time_signature_multiplier = \
                    measure.time_signature.implied_prolation
                written_adjustment = tuplet_multiplier / time_signature_multiplier
                tuplet._extract()
                measure._scale_contents(written_adjustment)
