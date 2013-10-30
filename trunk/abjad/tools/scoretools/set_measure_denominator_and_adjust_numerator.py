# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import durationtools
from abjad.tools import mathtools


# TODO: implement scoretools.set_measure_denominator_and_adjust_contents().
def set_measure_denominator_and_adjust_numerator(measure, denominator):
    r'''Set `measure` time signature `denominator` and multiply time signature numerator accordingly:

    ::

        >>> measure = Measure((3, 8), "c'8 d'8 e'8")
        >>> beam = spannertools.BeamSpanner()
        >>> attach(beam, measure.select_leaves())

    ..  doctest::

        >>> f(measure)
        {
            \time 3/8
            c'8 [
            d'8
            e'8 ]
        }

    ::

        >>> scoretools.set_measure_denominator_and_adjust_numerator(measure, 16)
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
    from abjad.tools import scoretools
    from abjad.tools.scoretools import attach

    if isinstance(measure, scoretools.Measure):
        # to allow iteration inside zero-update loop
        old_time_signature = measure.time_signature
        old_time_signature_pair = (old_time_signature.numerator, old_time_signature.denominator)
        new_time_signature = mathtools.NonreducedFraction(old_time_signature_pair)
        new_time_signature = new_time_signature.with_denominator(denominator)
        new_time_signature = marktools.TimeSignatureMark(new_time_signature)
        for mark in measure._get_marks(marktools.TimeSignatureMark):
            mark.detach()
        attach(new_time_signature, measure)

    return measure
