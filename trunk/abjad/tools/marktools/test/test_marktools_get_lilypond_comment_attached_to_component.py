from abjad import *
import py.test


def test_marktools_get_lilypond_comment_attached_to_component_01():

    note = Note("c'8")
    lilypond_comment = marktools.LilyPondComment('comment')(note)
    assert marktools.get_lilypond_comment_attached_to_component(note) is lilypond_comment


def test_marktools_get_lilypond_comment_attached_to_component_02():

    note = Note("c'8")
    assert py.test.raises(MissingMarkError, 'marktools.get_lilypond_comment_attached_to_component(note)')


def test_marktools_get_lilypond_comment_attached_to_component_03():

    note = Note("c'8")
    marktools.LilyPondComment('comment')(note)
    marktools.LilyPondComment('another comment')(note)
    assert py.test.raises(ExtraMarkError, 'marktools.get_lilypond_comment_attached_to_component(note)')
