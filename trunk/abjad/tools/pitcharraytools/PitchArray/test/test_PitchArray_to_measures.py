# -*- encoding: utf-8 -*-
from abjad import *


def test_PitchArray_to_measures_01():

    array = pitcharraytools.PitchArray([
        [1, (2, 1), ([-2, -1.5], 2)],
        [(7, 2), (6, 1), 1],
        ])

    '''
    [  ] [d'] [bf bqf     ]
    [g'      ] [fs'    ] []
    '''

    measures = array.to_measures()
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

    assert select(score).is_well_formed()
    assert testtools.compare(
        score.lilypond_format,
        "\\new Score <<\n\t\\new Staff {\n\t\t{\n\t\t\t\\time 4/8\n\t\t\tr8\n\t\t\td'8\n\t\t\t<bf bqf>4\n\t\t}\n\t}\n\t\\new Staff {\n\t\t{\n\t\t\t\\time 4/8\n\t\t\tg'4\n\t\t\tfs'8\n\t\t\tr8\n\t\t}\n\t}\n>>"
        )
