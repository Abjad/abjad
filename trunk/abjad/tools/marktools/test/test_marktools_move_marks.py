from abjad import *


def test_marktools_move_marks_01():

    staff = Staff(r'\clef "bass" c \staccato d e f')
        
    assert len(marktools.get_marks_attached_to_component(staff[0])) == 2
    assert len(marktools.get_marks_attached_to_component(staff[1])) == 0
    assert len(marktools.get_marks_attached_to_component(staff[2])) == 0
    assert len(marktools.get_marks_attached_to_component(staff[3])) == 0

    marktools.move_marks(staff[0], staff[2])

    assert len(marktools.get_marks_attached_to_component(staff[0])) == 0
    assert len(marktools.get_marks_attached_to_component(staff[1])) == 0
    assert len(marktools.get_marks_attached_to_component(staff[2])) == 2
    assert len(marktools.get_marks_attached_to_component(staff[3])) == 0
