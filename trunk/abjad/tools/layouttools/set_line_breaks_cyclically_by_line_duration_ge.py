from abjad.tools import measuretools


def set_line_breaks_cyclically_by_line_duration_ge(expr, line_duration, klass=None,
    adjust_eol=False, add_empty_bars=False):
    r'''Iterate `klass` instances in `expr` and accumulate prolated duration.
    Add line break after every total less than or equal to `line_duration`::

        >>> from abjad.tools import layouttools

    ::

        >>> t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    ::

        >>> f(t)
        \new Staff {
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

        >>> layouttools.set_line_breaks_cyclically_by_line_duration_ge(t, Duration(4, 8))
        >>> f(t)
        \new Staff {
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
                \break
            }
        }

    When ``klass=None`` set `klass` to measure.

    Set `adjust_eol` to ``True`` to include a magic Scheme incantation
    to move end-of-line LilyPond TimeSignature and BarLine grobs to
    the right.

    .. versionchanged:: 2.0
        renamed ``layout.line_break_every_prolated()`` to
        ``layout.set_line_breaks_cyclically_by_line_duration_ge()``.
    '''
    from abjad.tools.layouttools._line_break_every import _line_break_every

    if klass is None:
        klass = measuretools.Measure

    _line_break_every(
        expr, line_duration, klass, 'prolated', adjust_eol=adjust_eol,
        add_empty_bars=add_empty_bars)
