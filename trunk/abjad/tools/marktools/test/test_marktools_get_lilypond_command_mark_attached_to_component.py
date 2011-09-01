from abjad import *
import py.test


def test_marktools_get_lilypond_command_mark_attached_to_component_01():

    note = Note("c'8")
    lilypond_command_mark = marktools.LilyPondCommandMark('stemUp')(note)
    assert marktools.get_lilypond_command_mark_attached_to_component(note) is lilypond_command_mark


def test_marktools_get_lilypond_command_mark_attached_to_component_02():

    note = Note("c'8")
    assert py.test.raises(MissingMarkError, 'marktools.get_lilypond_command_mark_attached_to_component(note)')


def test_marktools_get_lilypond_command_mark_attached_to_component_03():

    note = Note("c'8")
    marktools.LilyPondCommandMark('stemUp')(note)
    marktools.LilyPondCommandMark('slurUp')(note)
    assert py.test.raises(ExtraMarkError, 'marktools.get_lilypond_command_mark_attached_to_component(note)')
