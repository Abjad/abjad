# -*- encoding: utf-8 -*-
from abjad import *


def test_Component__move_marks_01():

    staff = Staff(r'\clef "bass" c \staccato d e f')

    assert len(more(staff[0]).get_marks()) == 2
    assert len(more(staff[1]).get_marks()) == 0
    assert len(more(staff[2]).get_marks()) == 0
    assert len(more(staff[3]).get_marks()) == 0
    
    staff[0]._move_marks(staff[2])

    assert len(more(staff[0]).get_marks()) == 0
    assert len(more(staff[1]).get_marks()) == 0
    assert len(more(staff[2]).get_marks()) == 2
    assert len(more(staff[3]).get_marks()) == 0
