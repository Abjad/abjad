# -*- coding: utf-8 -*-
import abjad
from abjad import *


def test_instrumenttools_notes_and_chords_are_in_range_01():

    staff = abjad.Staff("c'8 r8 <d' fs'>8 r8")
    violin = abjad.instrumenttools.Violin()
    abjad.attach(violin, staff)

    assert abjad.instrumenttools.notes_and_chords_are_in_range(staff)


def test_instrumenttools_notes_and_chords_are_in_range_02():

    staff = abjad.Staff("c'8 r8 <d fs>8 r8")
    violin = abjad.instrumenttools.Violin()
    abjad.attach(violin, staff)

    assert not abjad.instrumenttools.notes_and_chords_are_in_range(staff)
