from abjad import *


def test_marktools_is_component_with_mark_attached_01():

    staff = Staff("c'2 d'2")
    marktools.Mark()(staff[0])

    assert marktools.is_component_with_mark_attached(staff[0])
    assert not marktools.is_component_with_mark_attached(staff[1])
