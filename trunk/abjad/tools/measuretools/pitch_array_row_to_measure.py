from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools.measuretools.Measure import Measure
from abjad.tools.pitcharraytools.PitchArrayRow.PitchArrayRow import PitchArrayRow


def pitch_array_row_to_measure(pitch_array_row, cell_duration_denominator = 8):
    r'''.. versionadded:: 2.0

    Change `pitch_array_row` to measure with meter
    `pitch_array_row.width` over `cell_duration_denominator`::

        abjad> from abjad.tools import pitcharraytools
        abjad> array = pitcharraytools.PitchArray([
        ...     [1, (2, 1), ([-2, -1.5], 2)],
        ...     [(7, 2), (6, 1), 1]])

    ::

        abjad> print array
        [  ] [d'] [bf bqf    ]
        [g'     ] [fs'   ] [ ]

    ::

        abjad> measure = measuretools.pitch_array_row_to_measure(array.rows[0])

    ::

        abjad> f(measure)
        {
            \time 4/8
            r8
            d'8
            <bf bqf>4
        }

    Return measure.
    '''
    from abjad.tools import leaftools

    if not isinstance(pitch_array_row, PitchArrayRow):
        raise TypeError('must be pitch array row.')

    meter = contexttools.TimeSignatureMark((pitch_array_row.width, cell_duration_denominator))
    measure = Measure(meter, [])
    basic_cell_duration = durationtools.Duration(1, cell_duration_denominator)
    measure_pitches, measure_durations = [], []
    for cell in pitch_array_row.cells:
        cell_pitches = cell.pitches
        if not cell_pitches:
            measure_pitches.append(None)
        elif len(cell_pitches) == 1:
            measure_pitches.append(cell_pitches[0])
        else:
            measure_pitches.append(cell_pitches)
        measure_duration = cell.width * basic_cell_duration
        measure_durations.append(measure_duration)
    leaves = leaftools.make_leaves(measure_pitches, measure_durations)
    measure.extend(leaves)

    return measure
