from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import timesignaturetools
from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr


def scale_contents_of_measures_in_expr(expr, multiplier = 1):
    '''.. versionadded:: 2.0

    Scale contents of measures in `expr` by `multiplier`.

    Iterate expr. For every measure in expr first multiply the measure
    meter by `multiplier` and then scale measure contents to fit
    the new meter.

    Extend ``containertools.scale_contents_of_container()``.

    Return none.
    '''

    from abjad.tools import containertools

    for measure in iterate_measures_forward_in_expr(expr):

        if multiplier == durationtools.Duration(1):
            continue

        if mathtools.is_nonnegative_integer_power_of_two(multiplier) and 1 <= multiplier:
            old_numerator = contexttools.get_effective_time_signature(measure).numerator
            old_denominator = contexttools.get_effective_time_signature(measure).denominator
            new_denominator = old_denominator / multiplier.numerator
            new_meter = contexttools.TimeSignatureMark((old_numerator, new_denominator))
        else:
            old_meter = contexttools.get_effective_time_signature(measure)
            old_denominator = old_meter.denominator
            old_duration = old_meter.duration
            new_duration = multiplier * old_duration
            new_meter = timesignaturetools.duration_and_possible_denominators_to_time_signature(
                new_duration, [old_denominator], multiplier.denominator)
        contexttools.detach_time_signature_marks_attached_to_component(measure)
        new_meter.attach(measure)

        contents_multiplier_denominator = \
            mathtools.greatest_power_of_two_less_equal(multiplier.denominator)
        contents_multiplier = durationtools.Duration(
            multiplier.numerator, contents_multiplier_denominator)
        containertools.scale_contents_of_container(measure, contents_multiplier)
