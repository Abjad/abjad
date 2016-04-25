# -*- coding: utf-8 -*-
from abjad import *


def test_instrumenttools_iterate_out_of_range_notes_and_chords_01():

    staff = Staff("c'8 r8 <d fs>8 r8")
    violin = instrumenttools.Violin()
    attach(violin, staff)

    leaves = instrumenttools.iterate_out_of_range_notes_and_chords(staff)
    leaves = list(leaves)

    assert len(leaves) == 1
    assert leaves[0] is staff[2]
