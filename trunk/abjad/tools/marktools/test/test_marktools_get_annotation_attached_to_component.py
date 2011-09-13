from abjad import *
import py.test


def test_marktools_get_annotation_attached_to_component_01():

    note = Note("c'8")
    annotation = marktools.Annotation('special information')(note)

    assert marktools.get_annotation_attached_to_component(note) is annotation


def test_marktools_get_annotation_attached_to_component_02():

    note = Note("c'8")

    assert py.test.raises(MissingMarkError, 'marktools.get_annotation_attached_to_component(note)')


def test_marktools_get_annotation_attached_to_component_03():

    note = Note("c'8")
    marktools.Annotation('special information')(note)
    marktools.Annotation('more special information')(note)

    assert py.test.raises(ExtraMarkError, 'marktools.get_annotation_attached_to_component(note)')
