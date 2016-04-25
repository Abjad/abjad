# -*- coding: utf-8 -*-
from abjad import *


def test_instrumenttools_notes_and_chords_are_in_range_01():

    staff = Staff("c'8 r8 <d' fs'>8 r8")
    violin = instrumenttools.Violin()
    attach(violin, staff)

    assert instrumenttools.notes_and_chords_are_in_range(staff)


def test_instrumenttools_notes_and_chords_are_in_range_02():

    staff = Staff("c'8 r8 <d fs>8 r8")
    violin = instrumenttools.Violin()
    attach(violin, staff)

    assert not instrumenttools.notes_and_chords_are_in_range(staff)
