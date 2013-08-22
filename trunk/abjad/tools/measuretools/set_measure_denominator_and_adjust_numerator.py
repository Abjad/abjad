# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import mathtools


# TODO: implement measuretools.set_measure_denominator_and_adjust_contents().
def set_measure_denominator_and_adjust_numerator(measure, denominator):
    r'''Set `measure` time signature `denominator` and multiply time signature numerator accordingly:

    ::

        >>> measure = Measure((3, 8), "c'8 d'8 e'8")
        >>> spannertools.BeamSpanner(measure.select_leaves())
        BeamSpanner(c'8, d'8, e'8)

    ..  doctest::

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

    ..  doctest::

        >>> f(measure)
        {
            \time 6/16
            c'8 [
            d'8
            e'8 ]
        }

    Leave `measure` contents unchanged.

    Return `measure`.
    '''
    from abjad.tools import measuretools

    if isinstance(measure, measuretools.Measure):
        # to allow iteration inside zero-update loop
        old_time_signature = measure.time_signature
        old_time_signature_pair = (old_time_signature.numerator, old_time_signature.denominator)
        new_time_signature = mathtools.NonreducedFraction(old_time_signature_pair)
        new_time_signature = new_time_signature.with_denominator(denominator)
        new_time_signature = contexttools.TimeSignatureMark(new_time_signature)
        for mark in measure._get_marks(contexttools.TimeSignatureMark):
            mark.detach()
        new_time_signature.attach(measure)

    return measure
