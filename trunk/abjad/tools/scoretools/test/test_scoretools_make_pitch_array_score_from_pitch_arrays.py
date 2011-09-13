from abjad import *
from abjad.tools import pitcharraytools


def test_scoretools_make_pitch_array_score_from_pitch_arrays_01():

    array_1 = pitcharraytools.PitchArray([
        [1, (2, 1), ([-2, -1.5], 2)],
        [(7, 2), (6, 1), 1],
        ])

    array_2 = pitcharraytools.PitchArray([
        [1, 1, 1],
        [1, 1, 1]])

    score = scoretools.make_pitch_array_score_from_pitch_arrays([array_1, array_2])

    r'''
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
    '''

    assert componenttools.is_well_formed_component(score)
    assert score.format == "\\new Score <<\n\t\\new StaffGroup <<\n\t\t\\new Staff {\n\t\t\t{\n\t\t\t\t\\time 4/8\n\t\t\t\tr8\n\t\t\t\td'8\n\t\t\t\t<bf bqf>4\n\t\t\t}\n\t\t\t{\n\t\t\t\t\\time 3/8\n\t\t\t\tr8\n\t\t\t\tr8\n\t\t\t\tr8\n\t\t\t}\n\t\t}\n\t\t\\new Staff {\n\t\t\t{\n\t\t\t\t\\time 4/8\n\t\t\t\tg'4\n\t\t\t\tfs'8\n\t\t\t\tr8\n\t\t\t}\n\t\t\t{\n\t\t\t\t\\time 3/8\n\t\t\t\tr8\n\t\t\t\tr8\n\t\t\t\tr8\n\t\t\t}\n\t\t}\n\t>>\n>>"
