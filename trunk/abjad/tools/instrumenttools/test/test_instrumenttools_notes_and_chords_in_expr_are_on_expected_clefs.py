from abjad import *


def test_instrumenttools_notes_and_chords_in_expr_are_on_expected_clefs_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.ClefMark('treble')(staff)
    instrumenttools.Violin()(staff)

    assert instrumenttools.notes_and_chords_in_expr_are_on_expected_clefs(staff)

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.ClefMark('alto')(staff)
    instrumenttools.Violin()(staff)

    assert not instrumenttools.notes_and_chords_in_expr_are_on_expected_clefs(staff)


def test_instrumenttools_notes_and_chords_in_expr_are_on_expected_clefs_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.ClefMark('treble')(staff)
    instrumenttools.Bassoon()(staff)

    assert not instrumenttools.notes_and_chords_in_expr_are_on_expected_clefs(staff)

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.ClefMark('alto')(staff)
    instrumenttools.Bassoon()(staff)

    assert not instrumenttools.notes_and_chords_in_expr_are_on_expected_clefs(staff)


def test_instrumenttools_notes_and_chords_in_expr_are_on_expected_clefs_03():

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.ClefMark('percussion')(staff)
    instrumenttools.Violin()(staff)

    assert instrumenttools.notes_and_chords_in_expr_are_on_expected_clefs(
        staff, percussion_clef_is_allowed = True)

    assert not instrumenttools.notes_and_chords_in_expr_are_on_expected_clefs(
        staff, percussion_clef_is_allowed = False)
