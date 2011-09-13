from abjad import *


def test_marktools_get_noncontext_marks_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.TimeSignatureMark((2, 4))(staff[0])
    articulation = marktools.Articulation('staccato')(staff[0])

    marks = marktools.get_noncontext_marks_attached_to_component(staff[0])

    assert marks == (articulation, )
