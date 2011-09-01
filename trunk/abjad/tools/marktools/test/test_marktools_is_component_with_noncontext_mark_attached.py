from abjad import *


def test_marktools_is_component_with_noncontext_mark_attached_01():
    
    note = Note("c'4")
    marktools.Articulation('staccato')(note)

    assert marktools.is_component_with_noncontext_mark_attached(note)

    note = Note("c'4")
    assert not marktools.is_component_with_noncontext_mark_attached(note)
