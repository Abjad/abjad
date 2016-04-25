# -*- coding: utf-8 -*-
from abjad import *


def test_instrumenttools_notes_and_chords_are_on_expected_clefs_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = Clef(name='treble')
    attach(clef, staff)
    violin = instrumenttools.Violin()
    attach(violin, staff)

    assert instrumenttools.notes_and_chords_are_on_expected_clefs(staff)

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = Clef(name='alto')
    attach(clef, staff)
    violin = instrumenttools.Violin()
    attach(violin, staff)

    assert not instrumenttools.notes_and_chords_are_on_expected_clefs(staff)


def test_instrumenttools_notes_and_chords_are_on_expected_clefs_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = Clef(name='treble')
    attach(clef, staff)
    bassoon = instrumenttools.Bassoon()
    attach(bassoon, staff)

    assert not instrumenttools.notes_and_chords_are_on_expected_clefs(staff)

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = Clef(name='alto')
    attach(clef, staff)
    bassoon = instrumenttools.Bassoon()
    attach(bassoon, staff)

    assert not instrumenttools.notes_and_chords_are_on_expected_clefs(staff)


def test_instrumenttools_notes_and_chords_are_on_expected_clefs_03():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = Clef(name='percussion')
    attach(clef, staff)
    violin = instrumenttools.Violin()
    attach(violin, staff)

    assert instrumenttools.notes_and_chords_are_on_expected_clefs(
        staff, percussion_clef_is_allowed = True)

    assert not instrumenttools.notes_and_chords_are_on_expected_clefs(
        staff, percussion_clef_is_allowed = False)
