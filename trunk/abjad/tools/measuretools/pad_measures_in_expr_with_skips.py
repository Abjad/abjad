from abjad.tools import skiptools


def pad_measures_in_expr_with_skips(expr, front, back, splice=False):
    r'''.. versionadded:: 2.0

    Pad measures in `expr` with skips.

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

        >>> t = Staff(measuretools.AnonymousMeasure("c'8 d'8") * 2)
        >>> front, back = Duration(1, 32), Duration(1, 64)
        >>> measuretools.pad_measures_in_expr_with_skips(t, front, back)

    ::

        >>> f(t)
        \new Staff {
            {
                \override Staff.TimeSignature #'stencil = ##f
                \time 19/64
                s32
                c'8
                d'8
                s64
                \revert Staff.TimeSignature #'stencil
            }
            {
                \override Staff.TimeSignature #'stencil = ##f
                s32
                c'8
                d'8
                s64
                \revert Staff.TimeSignature #'stencil
            }
        }

    Works when measures contain stacked voices. ::

        >>> measure = measuretools.DynamicMeasure(
        ...     Voice(notetools.make_repeated_notes(2)) * 2)
        >>> measure.is_parallel = True
        >>> t = Staff(measure * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
        >>> measuretools.pad_measures_in_expr_with_skips(
        ...     t, Duration(1, 32), Duration(1, 64))

    ::

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
    spanners over newly inserted skips::

        >>> t = measuretools.DynamicMeasure("c'8 d'8")
        >>> beamtools.BeamSpanner(t[:])
        BeamSpanner(c'8, d'8)
        >>> measuretools.pad_measures_in_expr_with_skips(
        ...     t, Duration(1, 32), Duration(1, 64), splice = True)

    ::

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

    .. versionchanged:: 2.0
        renamed ``layout.insert_measure_padding_skip()`` to
        ``measuretools.pad_measures_in_expr_with_skips()``.
    '''
    from abjad.tools.layouttools._insert_measure_padding import _insert_measure_padding

    klass_token = skiptools.Skip((1, 4))
    result = _insert_measure_padding(expr, front, back, klass_token, splice=splice)

    return result
