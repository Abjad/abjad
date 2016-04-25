# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArray_from_score_01():

    score = Score([])
    score.append(Staff("c'8 d'8 e'8 f'8 g'8 a'8"))
    score.append(Staff("c'4 d'4 e'4"))
    score.append(Staff("c'8 d'8 e'8 f'8 g'8 a'8"))

    r'''
    \new Score <<
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
        \new Staff {
            c'4
            d'4
            e'4
        }
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
    >>
    '''

    pitch_array = pitchtools.PitchArray.from_score(score, populate=False)

    '''
    [] [] [] [] [] []
    [      ] [      ] [      ]
    [] [] [] [] [] []
    '''

    assert pitch_array[0].cell_widths == (1, 1, 1, 1, 1, 1)
    assert pitch_array[1].cell_widths == (2, 2, 2)
    assert pitch_array[2].cell_widths == (1, 1, 1, 1, 1, 1)


def test_pitchtools_PitchArray_from_score_02():

    score = Score([])
    score.append(Staff("c'8 d'8 e'8 f'8"))
    score.append(Staff("c'4 d'4"))
    score.append(Staff(scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8") * 2))

    r'''
    \new Score <<
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        \new Staff {
            c'4
            d'4
        }
        \new Staff {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            \times 2/3 {
                c'8
                d'8
                e'8
            }
        }
    >>
    '''

    pitch_array = pitchtools.PitchArray.from_score(score, populate=False)

    '''
    [      ] [      ] [      ] [      ]
    [                 ] [                 ]
    [] [      ] [] [] [      ] []
    '''

    assert pitch_array[0].cell_widths == (2, 2, 2, 2)
    assert pitch_array[1].cell_widths == (4, 4)
    assert pitch_array[2].cell_widths == (1, 2, 1, 1, 2, 1)


def test_pitchtools_PitchArray_from_score_03():

    score = Score([])
    score.append(Staff("c'8 d'8 e'8 f'8 g'8 a'8"))
    score.append(Staff("c'4 d'4 e'4"))
    score.append(Staff("c'8 d'8 e'8 f'8 g'8 a'8"))

    r'''
    \new Score <<
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
        \new Staff {
            c'4
            d'4
            e'4
        }
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
    >>
    '''

    pitch_array = pitchtools.PitchArray.from_score(score, populate=True)

    '''
    [c'] [d'] [e'] [f'] [g'] [a']
    [c'      ] [d'      ] [e'      ]
    [c'] [d'] [e'] [f'] [g'] [a']
    '''

    assert pitch_array[0].pitches ==\
        pitchtools.list_named_pitches_in_expr(score[0])
    assert pitch_array[1].pitches ==\
        pitchtools.list_named_pitches_in_expr(score[1])
    assert pitch_array[2].pitches ==\
        pitchtools.list_named_pitches_in_expr(score[2])


def test_pitchtools_PitchArray_from_score_04():

    score = Score([])
    score.append(Staff("c'8 d'8 e'8 f'8"))
    score.append(Staff("c'4 d'4"))
    score.append(
        Staff(
            scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8") * 2))

    r'''
    \new Score <<
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        \new Staff {
            c'4
            d'4
        }
        \new Staff {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            \times 2/3 {
                c'8
                d'8
                e'8
            }
        }
    >>
    '''

    pitch_array = pitchtools.PitchArray.from_score(score, populate=True)

    '''
    [c'      ] [d'      ] [e'      ] [f'      ]
    [c'             ] [d'             ]
    [c'] [d'      ] [e'] [c'] [d'      ] [e']
    '''

    assert pitch_array[0].pitches ==\
        pitchtools.list_named_pitches_in_expr(score[0])
    assert pitch_array[1].pitches ==\
        pitchtools.list_named_pitches_in_expr(score[1])
    assert pitch_array[2].pitches ==\
        pitchtools.list_named_pitches_in_expr(score[2])
