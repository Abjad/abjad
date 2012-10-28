from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import mathtools


# TODO: implement measuretools.set_measure_denominator_and_adjust_contents().
def set_measure_denominator_and_adjust_numerator(measure, denominator):
    r'''.. versionadded:: 1.1

    Set `measure` time signature `denominator` and multiply time signature numerator accordingly::

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
        old_time_signature = contexttools.get_effective_time_signature(measure)
        old_time_signature_pair = (old_time_signature.numerator, old_time_signature.denominator)
        new_time_signature = mathtools.NonreducedFraction(old_time_signature_pair)
        new_time_signature = new_time_signature.with_denominator(denominator)
        new_time_signature = contexttools.TimeSignatureMark(new_time_signature)
        contexttools.detach_time_signature_marks_attached_to_component(measure)
        new_time_signature.attach(measure)

    return measure
