from abjad import *
from abjad.tools import pitcharraytools


def test_measuretools_pitch_array_to_measures_01():

    array = pitcharraytools.PitchArray([
        [1, (2, 1), ([-2, -1.5], 2)],
        [(7, 2), (6, 1), 1],
        ])

    '''
    [  ] [d'] [bf bqf     ]
    [g'      ] [fs'    ] []
    '''

    measures = measuretools.pitch_array_to_measures(array)
    score = Score(Staff([]) * 2)
    score[0].append(measures[0])
    score[1].append(measures[1])

    r'''
    \new Score <<
        \new Staff {
            {
                \time 4/8
                r8
                d'8
                <bf bqf>4
            }
        }
        \new Staff {
            {
                \time 4/8
                g'4
                fs'8
                r8
            }
        }
    >>
    '''

    assert componenttools.is_well_formed_component(score)
    assert score.format == "\\new Score <<\n\t\\new Staff {\n\t\t{\n\t\t\t\\time 4/8\n\t\t\tr8\n\t\t\td'8\n\t\t\t<bf bqf>4\n\t\t}\n\t}\n\t\\new Staff {\n\t\t{\n\t\t\t\\time 4/8\n\t\t\tg'4\n\t\t\tfs'8\n\t\t\tr8\n\t\t}\n\t}\n>>"
