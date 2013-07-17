from abjad import *


def test_marktools_move_marks_01():

    staff = Staff(r'\clef "bass" c \staccato d e f')

    assert len(staff[0].get_marks()) == 2
    assert len(staff[1].get_marks()) == 0
    assert len(staff[2].get_marks()) == 0
    assert len(staff[3].get_marks()) == 0
    
    marktools.move_marks(staff[0], staff[2])

    assert len(staff[0].get_marks()) == 0
    assert len(staff[1].get_marks()) == 0
    assert len(staff[2].get_marks()) == 2
    assert len(staff[3].get_marks()) == 0
