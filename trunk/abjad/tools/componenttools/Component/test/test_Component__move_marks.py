# -*- encoding: utf-8 -*-
from abjad import *


def test_Component__move_marks_01():

    staff = Staff(r'\clef "bass" c \staccato d e f')

    assert testtools.compare(
        staff,
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

    assert len(inspect(staff[0]).get_marks()) == 2
    assert len(inspect(staff[1]).get_marks()) == 0
    assert len(inspect(staff[2]).get_marks()) == 0
    assert len(inspect(staff[3]).get_marks()) == 0
    
    staff[0]._move_marks(staff[2])

    assert testtools.compare(
        staff,
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

    assert len(inspect(staff[0]).get_marks()) == 0
    assert len(inspect(staff[1]).get_marks()) == 0
    assert len(inspect(staff[2]).get_marks()) == 2
    assert len(inspect(staff[3]).get_marks()) == 0
