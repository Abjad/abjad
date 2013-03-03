def list_time_signatures_of_measures_in_expr(components):
    r'''.. versionadded:: 2.0

    List time signatures of measures in `expr`::

        >>> staff = Staff('abj: | 2/8 c8 d8 || 3/8 c8 d8 e8 || 4/8 c8 d8 e8 f8 |')

    ::

        >>> f(staff)
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

        >>> for x in measuretools.list_time_signatures_of_measures_in_expr(staff): x
        ...
        TimeSignatureMark((2, 8))(|2/8 c8 d8|)
        TimeSignatureMark((3, 8))(|3/8 c8 d8 e8|)
        TimeSignatureMark((4, 8))(|4/8 c8 d8 e8 f8|)

    Return list of zero or more time signatures.
    '''
    from abjad.tools import contexttools
    from abjad.tools import iterationtools

    # create empty list to hold result
    result = []

    # iterate measures and store time signature pairs
    for measure in iterationtools.iterate_measures_in_expr(components):
        time_signature = contexttools.get_effective_time_signature(measure)
        result.append(time_signature)

    # return result
    return result
