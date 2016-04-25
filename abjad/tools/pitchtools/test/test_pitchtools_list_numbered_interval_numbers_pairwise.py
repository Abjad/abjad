# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_list_numbered_interval_numbers_pairwise_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    staff = pitchtools.list_numbered_interval_numbers_pairwise(staff[:])

    assert staff == [2, 2, 1, 2, 2, 2, 1]

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    staff = pitchtools.list_numbered_interval_numbers_pairwise(
        staff[:],
        wrap=True,
        )

    assert staff == [2, 2, 1, 2, 2, 2, 1, -12]


def test_pitchtools_list_numbered_interval_numbers_pairwise_02():

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"), Note("g'8"),
        Note("a'8"), Note("b'8"), Note("c''8")]
    notes.reverse()
    t = pitchtools.list_numbered_interval_numbers_pairwise(notes)

    assert t == [-1, -2, -2, -2, -1, -2, -2]

    t = pitchtools.list_numbered_interval_numbers_pairwise(notes, wrap=True)

    assert t == [-1, -2, -2, -2, -1, -2, -2, 12]
