from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import mathtools


def multiply_contents_of_measures_in_expr(expr, n):
    r'''.. versionadded:: 1.1

    Multiply contents ``n - 1`` times and adjust time signature of every measure in `expr`::

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

        >>> measuretools.multiply_contents_of_measures_in_expr(measure, 3)

    ::

        >>> f(measure)
        {
            \time 9/8
            c'8 [
            d'8
            e'8 ]
            c'8 [
            d'8
            e'8 ]
            c'8 [
            d'8
            e'8 ]
        }

    Return none.
    '''
    from abjad.tools import contexttools
    from abjad.tools import iterationtools

    assert isinstance(n, int)
    assert 0 < n

    for measure in iterationtools.iterate_measures_in_expr(expr):
        old_time_signature = contexttools.get_effective_time_signature(measure)
        containertools.repeat_contents_of_container(measure, n)
        old_pair = (old_time_signature.numerator, old_time_signature.denominator)
        new_pair = mathtools.NonreducedFraction(old_pair)
        new_pair = new_pair.multiply_without_reducing(n)
        time_signature = contexttools.TimeSignatureMark(new_pair)
        contexttools.detach_time_signature_marks_attached_to_component(measure)
        time_signature.attach(measure)
