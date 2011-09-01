from abjad import *
import py.test


def test_marktools_get_mark_attached_to_component_01():

    note = Note("c'8")
    mark = marktools.Mark()(note)
    assert marktools.get_mark_attached_to_component(note) is mark


def test_marktools_get_mark_attached_to_component_02():

    note = Note("c'8")
    assert py.test.raises(MissingMarkError, 'marktools.get_mark_attached_to_component(note)')


def test_marktools_get_mark_attached_to_component_03():

    note = Note("c'8")
    marktools.Mark()(note)
    marktools.Mark()(note)
    assert py.test.raises(ExtraMarkError, 'marktools.get_mark_attached_to_component(note)')
