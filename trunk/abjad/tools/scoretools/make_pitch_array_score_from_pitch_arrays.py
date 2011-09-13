from abjad.tools.scoretools.Score import Score
from abjad.tools.stafftools.Staff import Staff
from abjad.tools.scoretools.StaffGroup.StaffGroup import StaffGroup


def make_pitch_array_score_from_pitch_arrays(pitch_arrays):
    r'''.. versionadded:: 2.0

    Make pitch-array score from `pitch_arrays`::

        abjad> from abjad.tools import pitcharraytools

        abjad> array_1 = pitcharraytools.PitchArray([
        ...   [1, (2, 1), ([-2, -1.5], 2)],
        ...   [(7, 2), (6, 1), 1]])

    ::

        abjad> array_2 = pitcharraytools.PitchArray([
        ...   [1, 1, 1],
        ...   [1, 1, 1]])

    ::

        abjad> score = scoretools.make_pitch_array_score_from_pitch_arrays([array_1, array_2])

    ::

        abjad> f(score)
        \new Score <<
            \new StaffGroup <<
                \new Staff {
                    {
                        \time 4/8
                        r8
                        d'8
                        <bf bqf>4
                    }
                    {
                        \time 3/8
                        r8
                        r8
                        r8
                    }
                }
                \new Staff {
                    {
                        \time 4/8
                        g'4
                        fs'8
                        r8
                    }
                    {
                        \time 3/8
                        r8
                        r8
                        r8
                    }
                }
            >>
        >>

    Create one staff per pitch-array row.

    Return score.
    '''

    from abjad.tools import measuretools

    score = Score([])
    staff_group = StaffGroup([])
    score.append(staff_group)
    number_staves = pitch_arrays[0].depth
    staves = Staff([]) * number_staves
    staff_group.extend(staves)

    for pitch_array in pitch_arrays:
        measures = measuretools.pitch_array_to_measures(pitch_array)
        for staff, measure in zip(staves, measures):
            staff.append(measure)

    return score
