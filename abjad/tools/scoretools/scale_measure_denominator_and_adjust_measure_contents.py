# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import durationtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach


def scale_measure_denominator_and_adjust_measure_contents(measure, factor):
    r'''Scales power-of-two `measure` to non-power-of-two measure
    with new denominator `factor`:

    ..  container:: example

        ::

            >>> measure = Measure((2, 8), "c'8 d'8")
            >>> measure.implicit_scaling = True
            >>> beam = spannertools.Beam()
            >>> attach(beam, measure[:])
            >>> show(measure) # doctest: +SKIP

        ..  doctest::

            >>> print(format(measure))
            {
                \time 2/8
                c'8 [
                d'8 ]
            }

        ::

            >>> scoretools.scale_measure_denominator_and_adjust_measure_contents(
            ...     measure, 3)
            Measure((3, 12), "c'8. d'8.", implicit_scaling=True)
            >>> show(measure) # doctest: +SKIP

        ..  doctest::

            >>> print(format(measure))
            {
                \time 3/12
                \scaleDurations #'(2 . 3) {
                    c'8. [
                    d'8. ]
                }
            }

    Treats new denominator `factor` like clever form of ``1``:
    ``3/3`` or ``5/5`` or ``7/7``, etc.

    Preserves `measure` duration.

    Derives new `measure` multiplier.

    Scales `measure` contents.

    Picks best new time signature.
    '''
    from abjad.tools import scoretools

    # save old time signature duration
    old_time_signature_duration = measure.time_signature.duration

    # find new time signature
    new_time_signature = \
        measure._duration_and_possible_denominators_to_time_signature(
        old_time_signature_duration,
        factor=factor,
        )

    # scale contents of measures in expr
    multiplier = new_time_signature.implied_prolation.reciprocal
    measure._scale(multiplier)

    # assign new time signature
    detach(indicatortools.TimeSignature, measure)
    attach(new_time_signature, measure)
    if new_time_signature.has_non_power_of_two_denominator:
        measure.implicit_scaling = True

    # return measure
    return measure