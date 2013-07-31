# -*- encoding: utf-8 -*-
from abjad import *


def test_Component__move_marks_01():

    staff = Staff(r'\clef "bass" c \staccato d e f')

    assert len(staff[0].get_marks()) == 2
    assert len(staff[1].get_marks()) == 0
    assert len(staff[2].get_marks()) == 0
    assert len(staff[3].get_marks()) == 0
    
    staff[0]._move_marks(staff[2])

    assert len(staff[0].get_marks()) == 0
    assert len(staff[1].get_marks()) == 0
    assert len(staff[2].get_marks()) == 2
    assert len(staff[3].get_marks()) == 0
