# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArrayInventory_to_score_01():

    array_1 = pitchtools.PitchArray([
        [1, (2, 1), ([-2, -1.5], 2)],
        [(7, 2), (6, 1), 1],
        ])

    array_2 = pitchtools.PitchArray([
        [1, 1, 1],
        [1, 1, 1]])

    arrays = [array_1, array_2]
    inventory = pitchtools.PitchArrayInventory(arrays)
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

    assert inspect_(score).is_well_formed()
    assert format(score) == stringtools.normalize(
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
        )
