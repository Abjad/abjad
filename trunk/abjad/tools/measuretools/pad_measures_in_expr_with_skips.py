# -*- encoding: utf-8 -*-
from abjad.tools import skiptools


# TODO: remove in favor of measuretools.pad_measures_in_expr()
def pad_measures_in_expr_with_skips(expr, front, back, splice=False):
    r'''Pad measures in `expr` with skips.

    Iterate all measures in `expr`. Insert skip with duration equal
    to `front` at beginning of each measure. Insert skip with
    duation aqual to `back` at end of each measure.

    Set `front` to a positive rational or none.
    Set `back` to a positive rational or none.

    Note that this function is designed to
    help create regularly spaced charts and tables of musical materials.
    This function makes most sense when used on anonymous measures
    and dynamic measures.

    ::

        >>> t = Staff(2 * Measure((2, 8), "c'8 d'8"))
        >>> front, back = Duration(1, 32), Duration(1, 64)
        >>> measuretools.pad_measures_in_expr_with_skips(t, front, back)

    ..  doctest::

        >>> f(t)
        \new Staff {
            {
                \time 19/64
                s32
                c'8
                d'8
                s64
            }
            {
                s32
                c'8
                d'8
                s64
            }
        }

    Works when measures contain stacked voices:

    ::

        >>> measure = Measure((2, 8), 2 * Voice(notetools.make_repeated_notes(2)))
        >>> measure.is_simultaneous = True
        >>> t = Staff(measure * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
        >>> measuretools.pad_measures_in_expr_with_skips(
        ...     t, Duration(1, 32), Duration(1, 64))

    ..  doctest::

        >>> f(t)
        \new Staff {
            <<
                \time 19/64
                \new Voice {
                    s32
                    c'8
                    d'8
                    s64
                }
                \new Voice {
                    s32
                    e'8
                    f'8
                    s64
                }
            >>
            <<
                \new Voice {
                    s32
                    g'8
                    a'8
                    s64
                }
                \new Voice {
                    s32
                    b'8
                    c''8
                    s64
                }
            >>
        }

    Set the optional `splice` keyword to ``True`` to extend edge
    spanners over newly inserted skips:

    ::

        >>> t = Measure((2, 8), "c'8 d'8")
        >>> spannertools.BeamSpanner(t[:])
        BeamSpanner(c'8, d'8)
        >>> measuretools.pad_measures_in_expr_with_skips(
        ...     t, Duration(1, 32), Duration(1, 64), splice=True)

    ..  doctest::

        >>> f(t)
        {
            \time 19/64
            s32 [
            c'8
            d'8
            s64 ]
        }

    Return none.

    Raise value error when `front` is neither a positive rational nor none.

    Raise value error when `back` is neither a positive rational nor none.
    '''
    from abjad.tools import measuretools

    class_token = skiptools.Skip((1, 4))
    result = measuretools.pad_measures_in_expr(
        expr, front, back, class_token, splice=splice)

    return result
