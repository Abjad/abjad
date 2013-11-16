# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import iterate


def move_full_measure_tuplet_prolation_to_measure_time_signature(expr):
    r'''Move prolation of full-measure tuplet to time signature of measure.

    Measures usually become non-power-of-two as as result:

    ::

        >>> t = Measure((2, 8), [scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")])
        >>> scoretools.move_full_measure_tuplet_prolation_to_measure_time_signature(t)

    ..  doctest::

        >>> print format(t)
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
    from abjad.tools import indicatortools

    for measure in iterate(expr).by_class(scoretools.Measure):
        if len(measure) == 1:
            if isinstance(measure[0], scoretools.Tuplet):
                tuplet = measure[0]
                tuplet_multiplier = tuplet.multiplier
                tuplet_denominator = tuplet_multiplier.denominator
                reduced_denominator = mathtools.remove_powers_of_two(tuplet_denominator)
                time_signature = measure.time_signature
                time_signature_rational = durationtools.Duration(
                    time_signature.numerator, time_signature.denominator)
                numerator = time_signature_rational.numerator * reduced_denominator
                denominator = time_signature_rational.denominator * reduced_denominator
                time_signature = indicatortools.TimeSignature((numerator, denominator))
                detach(indicatortools.TimeSignature, measure)
                attach(time_signature, measure)
                time_signature_multiplier = \
                    measure.time_signature.implied_prolation
                written_adjustment = tuplet_multiplier / time_signature_multiplier
                tuplet._extract()
                measure._scale_contents(written_adjustment)
