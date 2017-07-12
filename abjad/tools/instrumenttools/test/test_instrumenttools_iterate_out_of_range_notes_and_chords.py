# -*- coding: utf-8 -*-
import abjad


def test_instrumenttools_iterate_out_of_range_notes_and_chords_01():

    staff = abjad.Staff("c'8 r8 <d fs>8 r8")
    violin = abjad.instrumenttools.Violin()
    abjad.attach(violin, staff)

    leaves = abjad.instrumenttools.iterate_out_of_range_notes_and_chords(staff)
    leaves = list(leaves)

    assert len(leaves) == 1
    assert leaves[0] is staff[2]
