# -*- encoding: utf-8 -*-
from abjad.tools import scoretools


# TODO: remove in favor of layouttools.set_line_breaks_by_line_duration()
def set_line_breaks_by_line_duration_in_seconds_ge(
    expr, 
    line_duration,
    line_break_class=None, 
    add_empty_bars=False,
    ):
    r'''Iterate `line_break_class` instances in `expr` and 
    accumulate duration in seconds.

    Add line break after every total less than or equal to `line_duration`:

    ::

        >>> staff = Staff()
        >>> staff.append(Measure((2, 8), "c'8 d'8"))
        >>> staff.append(Measure((2, 8), "e'8 f'8"))
        >>> staff.append(Measure((2, 8), "g'8 a'8"))
        >>> staff.append(Measure((2, 8), "b'8 c''8"))
        >>> tempo = Tempo(Duration(1, 8), 44)
        >>> attach(tempo, staff, scope=Staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \tempo 8=44
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }

    ::

        >>> layouttools.set_line_breaks_by_line_duration_in_seconds_ge(
        ...     staff, Duration(6))
        >>> show(staff) # doctest: +SKIP

    ::

        >>> print format(staff)
        \new Staff {
            \tempo 8=44
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
                \break
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }

    When ``line_break_class=None`` set `line_break_class` to measure.
    '''
    from abjad.tools import layouttools

    if line_break_class is None:
        line_break_class = scoretools.Measure

    layouttools.set_line_breaks_by_line_duration(
        expr,
        line_duration,
        line_break_class,
        'seconds',
        add_empty_bars=add_empty_bars,
        )
