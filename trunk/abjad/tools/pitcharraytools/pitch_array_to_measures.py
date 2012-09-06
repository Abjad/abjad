from abjad.tools import measuretools


def pitch_array_to_measures(pitch_array, cell_duration_denominator=8):
    r'''.. versionadded:: 2.0

    Change `pitch_array` to measures with meters
    `row.width` over `cell_duration_denominator` for each
    row in `pitch_array`::

        >>> from abjad.tools import pitcharraytools
        >>> array = pitcharraytools.PitchArray([
        ...     [1, (2, 1), ([-2, -1.5], 2)],
        ...     [(7, 2), (6, 1), 1]])

    ::

        >>> print array
        [  ] [d'] [bf bqf    ]
        [g'     ] [fs'   ] [ ]

    ::

        >>> pitcharraytools.pitch_array_to_measures(array)
        [Measure(4/8, [r8, d'8, <bf bqf>4]), Measure(4/8, [g'4, fs'8, r8])]
        >>> for measure in _:
        ...     f(measure)
        ...
        {
            \time 4/8
            r8
            d'8
            <bf bqf>4
        }
        {
            \time 4/8
            g'4
            fs'8
            r8
        }

    Return list of measures.
    '''
    from abjad.tools import pitcharraytools

    measures = []
    for row in pitch_array.rows:
        measure = pitcharraytools.pitch_array_row_to_measure(row, cell_duration_denominator)
        measures.append(measure)

    return measures
