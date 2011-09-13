from abjad.tools import mathtools
from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr
from abjad.tools import durationtools


def move_prolation_of_full_measure_tuplet_to_meter_of_measure(expr):
    r'''.. versionadded:: 1.1

    Move prolation of full-measure tuplet to meter of measure.

    Measures usually become nonbinary as as result::

        abjad> t = Measure((2, 8), [tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")])
        abjad> measuretools.move_prolation_of_full_measure_tuplet_to_meter_of_measure(t)

    ::

        abjad> f(t)
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
        ``measuretools.move_prolation_of_full_measure_tuplet_to_meter_of_measure()``.
    '''
    from abjad.tools.tuplettools.Tuplet import Tuplet
    from abjad.tools import componenttools
    from abjad.tools import contexttools
    from abjad.tools import containertools

    for measure in iterate_measures_forward_in_expr(expr):
        if len(measure) == 1:
            if isinstance(measure[0], Tuplet):
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
