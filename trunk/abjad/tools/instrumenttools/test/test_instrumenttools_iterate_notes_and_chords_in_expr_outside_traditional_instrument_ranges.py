from abjad import *


def test_instrumenttools_iterate_notes_and_chords_in_expr_outside_traditional_instrument_ranges_01():

    staff = Staff("c'8 r8 <d fs>8 r8")
    instrumenttools.Violin()(staff)

    leaves = instrumenttools.iterate_notes_and_chords_in_expr_outside_traditional_instrument_ranges(staff)
    leaves = list(leaves)

    assert len(leaves) == 1
    assert leaves[0] is staff[2]
