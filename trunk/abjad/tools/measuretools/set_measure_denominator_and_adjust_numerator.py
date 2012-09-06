from abjad.tools import contexttools
from abjad.tools import durationtools


# TODO: implement measuretools.set_measure_denominator_and_adjust_contents().
def set_measure_denominator_and_adjust_numerator(measure, denominator):
    r'''.. versionadded:: 1.1

    Set `measure` meter `denominator` and multiply meter numerator accordingly::

        >>> measure = Measure((3, 8), "c'8 d'8 e'8")
        >>> beamtools.BeamSpanner(measure.leaves)
        BeamSpanner(c'8, d'8, e'8)

    ::

        >>> f(measure)
        {
            \time 3/8
            c'8 [
            d'8
            e'8 ]
        }

    ::

        >>> measuretools.set_measure_denominator_and_adjust_numerator(measure, 16)
        Measure(6/16, [c'8, d'8, e'8])

    ::

        >>> f(measure)
        {
            \time 6/16
            c'8 [
            d'8
            e'8 ]
        }

    Leave `measure` contents unchanged.

    Return `measure`.

    .. versionchanged:: 2.0
        renamed ``measuretools.set_measure_denominator_and_multiply_numerator()`` to
        ``measuretools.set_measure_denominator_and_adjust_numerator()``.
    '''
    from abjad.tools import measuretools

    if isinstance(measure, measuretools.Measure):
        # to allow iteration inside zero-update loop
        old_meter = contexttools.get_effective_time_signature(measure)
        old_meter_pair = (old_meter.numerator, old_meter.denominator)
        new_meter = durationtools.rational_to_duration_pair_with_specified_integer_denominator(
            old_meter_pair, denominator)
        new_meter = contexttools.TimeSignatureMark(new_meter)
        contexttools.detach_time_signature_marks_attached_to_component(measure)
        new_meter.attach(measure)

    return measure
