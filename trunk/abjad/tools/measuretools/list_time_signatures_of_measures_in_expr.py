def list_time_signatures_of_measures_in_expr(components):
    r'''.. versionadded:: 2.0

    List time signatures of measures in `expr`::

        abjad> from abjad.tools import timesignaturetools

    ::

        abjad> staff = Staff([Measure((2, 8), "c8 d8"), Measure((3, 8), "c8 d8 e8"), Measure((4, 8), "c8 d8 e8 f8")])

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 2/8
                c8
                d8
            }
            {
                \time 3/8
                c8
                d8
                e8
            }
            {
                \time 4/8
                c8
                d8
                e8
                f8
            }
        }

    ::

        abjad> measuretools.list_time_signatures_of_measures_in_expr(staff)
        [TimeSignatureMark((2, 8))(|2/8, c8, d8|), TimeSignatureMark((3, 8))(|3/8, c8, d8, e8|), TimeSignatureMark((4, 8))(|4/8, c8, d8, e8, f8|)]

    Return list of zero or more time signatures.

    .. versionchanged:: 2.0
        renamed ``measuretools.list_time_signatures_of_mesures_in_expr()`` to
        ``measuretools.list_time_signatures_of_measures_in_expr()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import contexttools
    from abjad.tools import measuretools

    # make sure components is a Python list of Abjad components
    #assert componenttools.all_are_components(components)

    # create empty list to hold result
    result = []

    # iterate measures and store meter pairs
    for measure in measuretools.iterate_measures_forward_in_expr(components):
        meter = contexttools.get_effective_time_signature(measure)
        #pair = (meter.numerator, meter.denominator)
        #result.append(pair)
        result.append(meter)

    # return result
    return result
