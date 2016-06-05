# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Component__move_indicators_01():

    staff = Staff(r'\clef "bass" c \staccato d e f')

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \clef "bass"
            c4 -\staccato
            d4
            e4
            f4
        }
        '''
        )

    assert len(inspect_(staff[0]).get_indicators()) == 2
    assert len(inspect_(staff[1]).get_indicators()) == 0
    assert len(inspect_(staff[2]).get_indicators()) == 0
    assert len(inspect_(staff[3]).get_indicators()) == 0

    staff[0]._move_indicators(staff[2])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c4
            d4
            \clef "bass"
            e4 -\staccato
            f4
        }
        '''
        )

    assert len(inspect_(staff[0]).get_indicators()) == 0
    assert len(inspect_(staff[1]).get_indicators()) == 0
    assert len(inspect_(staff[2]).get_indicators()) == 2
    assert len(inspect_(staff[3]).get_indicators()) == 0
