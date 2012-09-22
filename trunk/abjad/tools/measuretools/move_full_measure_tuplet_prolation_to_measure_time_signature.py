from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import mathtools


def move_full_measure_tuplet_prolation_to_measure_time_signature(expr):
    r'''.. versionadded:: 1.1

    Move prolation of full-measure tuplet to meter of measure.

    Measures usually become nonbinary as as result::

        >>> t = Measure((2, 8), [tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")])
        >>> measuretools.move_full_measure_tuplet_prolation_to_measure_time_signature(t)

    ::

        >>> f(t)
        {
            \time 3/12
            \scaleDurations #'(2 . 3) {
                c'8
                d'8
                e'8
            }
        }

    Return none.

    .. versionchanged:: 2.0
        renamed ``measuretools.subsume()`` to
        ``measuretools.move_full_measure_tuplet_prolation_to_measure_time_signature()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import contexttools
    from abjad.tools import iterationtools
    from abjad.tools import tuplettools

    for measure in iterationtools.iterate_measures_in_expr(expr):
        if len(measure) == 1:
            if isinstance(measure[0], tuplettools.Tuplet):
                tuplet = measure[0]
                tuplet_multiplier = tuplet.multiplier
                tuplet_denominator = tuplet_multiplier.denominator
                reduced_denominator = mathtools.remove_powers_of_two(tuplet_denominator)
                meter = contexttools.get_effective_time_signature(measure)
                meter_rational = durationtools.Duration(meter.numerator, meter.denominator)
                numerator = meter_rational.numerator * reduced_denominator
                denominator = meter_rational.denominator * reduced_denominator
                time_signature = contexttools.TimeSignatureMark((numerator, denominator))
                contexttools.detach_time_signature_marks_attached_to_component(measure)
                time_signature.attach(measure)
                meter_multiplier = contexttools.get_effective_time_signature(measure).multiplier
                written_adjustment = tuplet_multiplier / meter_multiplier
                componenttools.move_parentage_and_spanners_from_components_to_components(
                    [tuplet], tuplet[:])
                containertools.scale_contents_of_container(measure, written_adjustment)
