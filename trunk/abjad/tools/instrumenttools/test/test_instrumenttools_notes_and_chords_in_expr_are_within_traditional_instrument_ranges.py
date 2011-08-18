from abjad import *


def test_instrumenttools_notes_and_chords_in_expr_are_within_traditional_instrument_ranges_01():

    staff = Staff("c'8 r8 <d' fs'>8 r8")
    instrumenttools.Violin()(staff)

    assert instrumenttools.notes_and_chords_in_expr_are_within_traditional_instrument_ranges(staff)


def test_instrumenttools_notes_and_chords_in_expr_are_within_traditional_instrument_ranges_02():

    staff = Staff("c'8 r8 <d fs>8 r8")
    instrumenttools.Violin()(staff)

    assert not instrumenttools.notes_and_chords_in_expr_are_within_traditional_instrument_ranges(staff)
