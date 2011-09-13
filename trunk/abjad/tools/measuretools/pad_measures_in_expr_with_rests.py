def pad_measures_in_expr_with_rests(expr, front, back, splice = False):
    r'''.. versionadded:: 1.1

    Pad measures in `expr` with rests.

    Iterate all measures in `expr`. Insert rest with duration equal
    to `front` at beginning of each measure. Insert rest with
    duation aqual to `back` at end of each measure.

    Set `front` to a positive rational or none.
    Set `back` to a positive rational or none.

    Note that this function is designed to
    help create regularly spaced charts and tables of musical materials.
    This function makes most sense when used on anonymous measures or
    dynamic measures.

    ::

        abjad> t = Staff(measuretools.AnonymousMeasure("c'8 d'8") * 2)
        abjad> front, back = Duration(1, 32), Duration(1, 64)
        abjad> measuretools.pad_measures_in_expr_with_rests(t, front, back)

    ::

        abjad> f(t)
        \new Staff {
            {
                \override Staff.TimeSignature #'stencil = ##f
                \time 19/64
                r32
                c'8
                d'8
                r64
                \revert Staff.TimeSignature #'stencil
            }
            {
                \override Staff.TimeSignature #'stencil = ##f
                \time 19/64
                r32
                c'8
                d'8
                r64
                \revert Staff.TimeSignature #'stencil
            }
        }

    Works when measures contain stacked voices::

        abjad> measure = measuretools.DynamicMeasure(Voice(notetools.make_repeated_notes(2)) * 2)
        abjad> measure.is_parallel = True
        abjad> t = Staff(measure * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
        abjad> measuretools.pad_measures_in_expr_with_rests(t, Duration(1, 32), Duration(1, 64))

    ::

        abjad> f(t)
        \new Staff {
            <<
                \time 19/64
                \new Voice {
                    r32
                    c'8
                    d'8
                    r64
                }
                \new Voice {
                    r32
                    e'8
                    f'8
                    r64
                }
            >>
            <<
                \time 19/64
                \new Voice {
                    r32
                    g'8
                    a'8
                    r64
                }
                \new Voice {
                    r32
                    b'8
                    c''8
                    r64
                }
            >>
        }

    Set the optional `splice` keyword to ``True`` to extend edge
    spanners over newly inserted rests::

        abjad> t = measuretools.DynamicMeasure("c'8 d'8")
        abjad> spannertools.BeamSpanner(t[:])
        BeamSpanner(c'8, d'8)
        abjad> measuretools.pad_measures_in_expr_with_rests(t, Duration(1, 32), Duration(1, 64), splice = True)

    ::

        abjad> f(t)
        {
            \time 19/64
            r32 [
            c'8
            d'8
            r64 ]
        }

    Return none.

    Raise value when `front` is neither a positive rational nor none.

    Raise value when `back` is neither a positive rational nor none.

    .. versionchanged:: 2.0
        renamed ``layout.insert_measure_padding_rest()`` to
        ``measuretools.pad_measures_in_expr_with_rests()``.
    '''
    from abjad.tools.layouttools._insert_measure_padding import _insert_measure_padding
    from abjad.tools.resttools.Rest import Rest

    klass_token = Rest((1, 4))
    result = _insert_measure_padding(expr, front, back, klass_token, splice = splice)
    return result
