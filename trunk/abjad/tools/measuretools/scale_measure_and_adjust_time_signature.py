from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import mathtools


def scale_measure_and_adjust_time_signature(measure, multiplier=1):
    r'''.. versionadded:: 2.0

    Scale `measure` by `multiplier` and adjust meter::

        >>> t = Measure((3, 8), "c'8 d'8 e'8")
        >>> measuretools.scale_measure_and_adjust_time_signature(t, Duration(2, 3))
        Measure(3/12, [c'8, d'8, e'8])

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

    Return `measure`.
    '''
    from abjad.tools import contexttools

    if multiplier == 0:
        raise ZeroDivisionError

    old_meter = contexttools.get_effective_time_signature(measure)
    old_pair = (old_meter.numerator, old_meter.denominator)
    old_multiplier = old_meter.multiplier
    old_multiplier_pair = (old_multiplier.numerator, old_multiplier.denominator)

    multiplied_pair = mathtools.NonreducedFraction(old_multiplier_pair)
    multiplied_pair = multiplied_pair.multiply_without_reducing(multiplier)
    multiplied_pair = multiplied_pair.pair
    reduced_pair = mathtools.NonreducedFraction(old_multiplier_pair)
    reduced_pair = reduced_pair.multiply_with_cross_cancelation(multiplier)
    reduced_pair = reduced_pair.pair

    if reduced_pair != multiplied_pair:
        new_pair = mathtools.NonreducedFraction(old_pair)
        new_pair = new_pair.multiply_with_numerator_preservation(multiplier)
        new_meter = contexttools.TimeSignatureMark(new_pair)
        contexttools.detach_time_signature_marks_attached_to_component(measure)
        new_meter.attach(measure)
        remaining_multiplier = durationtools.Duration(reduced_pair)
        if remaining_multiplier != durationtools.Duration(1):
            containertools.scale_contents_of_container(measure, remaining_multiplier)
    elif componenttools.all_are_components_scalable_by_multiplier(measure[:], multiplier):
        containertools.scale_contents_of_container(measure, multiplier)
        if old_meter.is_nonbinary or not mathtools.is_nonnegative_integer_power_of_two(multiplier):
            new_pair = mathtools.NonreducedFraction(old_pair)
            new_pair = new_pair.multiply_with_cross_cancelation(multiplier)
            new_pair = new_pair.pair
        # multiplier is a negative power of two, like 1/2, 1/4, etc.
        elif multiplier < durationtools.Duration(0):
            new_pair = durationtools.multiply_duration_pair(old_pair, multiplier)
        # multiplier is a nonnegative power of two, like 0, 1, 2, 4, etc.
        elif durationtools.Duration(0) < multiplier:
            new_pair = mathtools.NonreducedFraction(old_pair)
            new_pair = new_pair.multiply_with_numerator_preservation(multiplier)
        elif multiplier == durationtools.Duration(0):
            raise ZeroDivisionError
        new_meter = contexttools.TimeSignatureMark(new_pair)
        contexttools.detach_time_signature_marks_attached_to_component(measure)
        new_meter.attach(measure)
    else:
        new_pair = mathtools.NonreducedFraction(old_pair)
        new_pair = new_pair.multiply_with_numerator_preservation(multiplier)
        new_meter = contexttools.TimeSignatureMark(new_pair)
        contexttools.detach_time_signature_marks_attached_to_component(measure)
        new_meter.attach(measure)
        remaining_multiplier = multiplier / new_meter.multiplier
        if remaining_multiplier != durationtools.Duration(1):
            containertools.scale_contents_of_container(measure, remaining_multiplier)
    return measure
