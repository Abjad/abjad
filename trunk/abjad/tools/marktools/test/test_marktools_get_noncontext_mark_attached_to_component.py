from abjad import *
import py.test


def test_marktools_get_noncontext_mark_attached_to_component_01():

    note = Note("c'8")
    noncontext_mark = marktools.Articulation('staccato')(note)
    assert marktools.get_noncontext_mark_attached_to_component(note) is noncontext_mark


def test_marktools_get_noncontext_mark_attached_to_component_02():

    note = Note("c'8")
    assert py.test.raises(MissingMarkError, 'marktools.get_noncontext_mark_attached_to_component(note)')


def test_marktools_get_noncontext_mark_attached_to_component_03():

    note = Note("c'8")
    marktools.Articulation('staccato')(note)
    marktools.Articulation('marcato')(note)
    assert py.test.raises(ExtraMarkError, 'marktools.get_noncontext_mark_attached_to_component(note)')
