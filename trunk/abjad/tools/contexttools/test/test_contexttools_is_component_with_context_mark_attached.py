from abjad import *


def test_contexttools_is_component_with_context_mark_attached_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.TimeSignatureMark((4, 8))(staff[0])

    assert contexttools.is_component_with_context_mark_attached(staff[0])
    assert not contexttools.is_component_with_context_mark_attached(staff[1])
    assert not contexttools.is_component_with_context_mark_attached(staff[2])
    assert not contexttools.is_component_with_context_mark_attached(staff[3])

    assert not contexttools.is_component_with_context_mark_attached(staff)
