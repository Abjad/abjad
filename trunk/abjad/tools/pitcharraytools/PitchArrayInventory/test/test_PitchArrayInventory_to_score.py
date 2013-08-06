# -*- encoding: utf-8 -*-
from abjad import *


def test_PitchArrayInventory_to_score_01():

    array_1 = pitcharraytools.PitchArray([
        [1, (2, 1), ([-2, -1.5], 2)],
        [(7, 2), (6, 1), 1],
        ])

    array_2 = pitcharraytools.PitchArray([
        [1, 1, 1],
        [1, 1, 1]])

    arrays = [array_1, array_2]
    inventory = pitcharraytools.PitchArrayInventory(arrays)
    score = inventory.to_score()

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

    assert select(score).is_well_formed()
    assert testtools.compare(
        score.lilypond_format,
        "\\new Score <<\n\t\\new StaffGroup <<\n\t\t\\new Staff {\n\t\t\t{\n\t\t\t\t\\time 4/8\n\t\t\t\tr8\n\t\t\t\td'8\n\t\t\t\t<bf bqf>4\n\t\t\t}\n\t\t\t{\n\t\t\t\t\\time 3/8\n\t\t\t\tr8\n\t\t\t\tr8\n\t\t\t\tr8\n\t\t\t}\n\t\t}\n\t\t\\new Staff {\n\t\t\t{\n\t\t\t\t\\time 4/8\n\t\t\t\tg'4\n\t\t\t\tfs'8\n\t\t\t\tr8\n\t\t\t}\n\t\t\t{\n\t\t\t\t\\time 3/8\n\t\t\t\tr8\n\t\t\t\tr8\n\t\t\t\tr8\n\t\t\t}\n\t\t}\n\t>>\n>>"
        )
