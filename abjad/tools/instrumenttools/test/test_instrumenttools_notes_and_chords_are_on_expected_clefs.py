# -*- coding: utf-8 -*-
import abjad
from abjad import *


def test_instrumenttools_notes_and_chords_are_on_expected_clefs_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    clef = abjad.Clef(name='treble')
    abjad.attach(clef, staff)
    violin = abjad.instrumenttools.Violin()
    abjad.attach(violin, staff)

    assert abjad.instrumenttools.notes_and_chords_are_on_expected_clefs(staff)

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    clef = abjad.Clef(name='alto')
    abjad.attach(clef, staff)
    violin = abjad.instrumenttools.Violin()
    abjad.attach(violin, staff)

    assert not abjad.instrumenttools.notes_and_chords_are_on_expected_clefs(staff)


def test_instrumenttools_notes_and_chords_are_on_expected_clefs_02():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    clef = abjad.Clef(name='treble')
    abjad.attach(clef, staff)
    bassoon = abjad.instrumenttools.Bassoon()
    abjad.attach(bassoon, staff)

    assert not abjad.instrumenttools.notes_and_chords_are_on_expected_clefs(staff)

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    clef = abjad.Clef(name='alto')
    abjad.attach(clef, staff)
    bassoon = abjad.instrumenttools.Bassoon()
    abjad.attach(bassoon, staff)

    assert not abjad.instrumenttools.notes_and_chords_are_on_expected_clefs(staff)


def test_instrumenttools_notes_and_chords_are_on_expected_clefs_03():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    clef = abjad.Clef(name='percussion')
    abjad.attach(clef, staff)
    violin = abjad.instrumenttools.Violin()
    abjad.attach(violin, staff)

    assert abjad.instrumenttools.notes_and_chords_are_on_expected_clefs(
        staff, percussion_clef_is_allowed = True)

    assert not abjad.instrumenttools.notes_and_chords_are_on_expected_clefs(
        staff, percussion_clef_is_allowed = False)
