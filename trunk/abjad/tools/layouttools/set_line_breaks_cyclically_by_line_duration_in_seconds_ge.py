from abjad.tools import measuretools


def set_line_breaks_cyclically_by_line_duration_in_seconds_ge(expr, line_duration,
    klass=None, adjust_eol=False, add_empty_bars=False):
    r'''Iterate `klass` instances in `expr` and accumulate duration in seconds.
    Add line break after every total less than or equal to `line_duration`::

        >>> t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
        >>> tempo_mark = contexttools.TempoMark(Duration(1, 8), 44, target_context = Staff)(t)

    ::

        >>> f(t)
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

        >>> layouttools.set_line_breaks_cyclically_by_line_duration_in_seconds_ge(t, Duration(6))
        >>> f(t)
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

    When ``klass=None`` set `klass` to measure.

    Set ``adjust_eol = True`` to include a magic Scheme incantation
    to move end-of-line LilyPond TimeSignature and BarLine grobs to
    the right.
    '''
    from abjad.tools.layouttools._line_break_every import _line_break_every

    if klass is None:
        klass = measuretools.Measure

    _line_break_every(
        expr, line_duration, klass, 'seconds', adjust_eol=adjust_eol,
        add_empty_bars=add_empty_bars)
