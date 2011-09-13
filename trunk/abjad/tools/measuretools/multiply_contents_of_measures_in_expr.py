from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr
from abjad.tools import durationtools


def multiply_contents_of_measures_in_expr(expr, n):
    r'''.. versionadded:: 1.1

    Multiply contents ``n - 1`` times and adjust meter of every measure in `expr`::

        abjad> measure = Measure((3, 8), "c'8 d'8 e'8")
        abjad> spannertools.BeamSpanner(measure.leaves)
        BeamSpanner(c'8, d'8, e'8)

    ::

        abjad> f(measure)
        {
            \time 3/8
            c'8 [
            d'8
            e'8 ]
        }

    ::

        abjad> measuretools.multiply_contents_of_measures_in_expr(measure, 3)

    ::

        abjad> f(measure)
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

    .. versionchanged:: 2.0
        renamed ``measuretools.spin()`` to
        ``measuretools.multiply_contents_of_measures_in_expr()``.
    '''

    from abjad.tools import containertools
    assert isinstance(n, int)
    assert 0 < n

    for measure in iterate_measures_forward_in_expr(expr):
        old_meter = contexttools.get_effective_time_signature(measure)
        containertools.repeat_contents_of_container(measure, n)
        old_pair = (old_meter.numerator, old_meter.denominator)
        new_pair = durationtools.multiply_duration_pair(old_pair, durationtools.Duration(n))
        time_signature = contexttools.TimeSignatureMark(new_pair)
        contexttools.detach_time_signature_marks_attached_to_component(measure)
        time_signature.attach(measure)
