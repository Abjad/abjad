from abjad import *


def test_marktools_detach_marks_attached_to_components_in_expr_01():

    staff = Staff("c'4 \staccato d' \marcato e' \staccato f' \marcato")
    assert len(marktools.get_marks_attached_to_components_in_expr(staff)) == 4

    marks = marktools.detach_marks_attached_to_components_in_expr(staff)
    assert marks == (
        marktools.Articulation('staccato'), 
        marktools.Articulation('marcato'), 
        marktools.Articulation('staccato'), 
        marktools.Articulation('marcato'))

    assert not len(marktools.get_marks_attached_to_components_in_expr(staff))
