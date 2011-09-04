from abjad import *


def test_marktools_detach_marks_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.leaves)
    marktools.Articulation('^')(staff[0])
    marktools.LilyPondComment('comment 1')(staff[0])
    marktools.LilyPondCommandMark('slurUp')(staff[0])
    marks = marktools.get_marks_attached_to_component(staff[0])
    assert len(marks) == 3

    marktools.detach_marks_attached_to_component(staff[0])
    marks = marktools.get_marks_attached_to_component(staff[0])
    assert len(marks) == 0
