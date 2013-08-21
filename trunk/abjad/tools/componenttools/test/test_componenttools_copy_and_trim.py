# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_copy_and_trim_01():
    r'''Container.
    '''

    container = Container("c'8 d'8 e'8")
    new_container = componenttools.copy_and_trim(
        container, Offset(0), Offset(3, 16))

    assert testtools.compare(
        new_container,
        r'''
        {
            c'8
            d'16
        }
        '''
        )

    assert select(new_container).is_well_formed()


def test_componenttools_copy_and_trim_02():
    r'''Container with rest.
    '''

    container = Container("c'8 r8 e'8")
    new_container = componenttools.copy_and_trim(
        container, Offset(0), Offset(3, 16))

    assert testtools.compare(
        new_container,
        r'''
        {
            c'8
            r16
        }
        '''
        )

    assert select(new_container).is_well_formed()


def test_componenttools_copy_and_trim_03():
    r'''Copy measure.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")
    new_measure = componenttools.copy_and_trim(
        measure, Offset(0), Offset(3, 16))

    assert testtools.compare(
        new_measure,
        r'''
        {
            \time 3/16
            c'8
            d'16
        }
        '''
        )

    assert select(new_measure).is_well_formed()


def test_componenttools_copy_and_trim_04():
    r'''Fixed-duration tuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(1, 4), "c'8 d'8 e'8")
    new_tuplet = componenttools.copy_and_trim(
        tuplet, Offset(0), Offset(1, 8))

    assert testtools.compare(
        new_tuplet,
        r'''
        \times 2/3 {
            c'8
            d'16
        }
        '''
        )

    assert select(new_tuplet).is_well_formed()


def test_componenttools_copy_and_trim_05():
    r'''Tuplet.
    '''

    tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
    new_tuplet = componenttools.copy_and_trim(
        tuplet, Offset(0), Offset(1, 8))

    assert testtools.compare(
        new_tuplet,
        r'''
        \times 2/3 {
            c'8
            d'16
        }
        '''
        )

    assert select(new_tuplet).is_well_formed()


def test_componenttools_copy_and_trim_06():
    r'''Voice.
    '''

    voice = Voice("c'8 d'8 e'8")
    new_voice = componenttools.copy_and_trim(
        voice, Offset(0), Offset(3, 16))

    assert testtools.compare(
        new_voice,
        r'''
        \new Voice {
            c'8
            d'16
        }
        '''
        )

    assert select(new_voice).is_well_formed()


def test_componenttools_copy_and_trim_07():
    r'''Staff.
    '''

    staff = Staff("c'8 d'8 e'8")
    new_staff = componenttools.copy_and_trim(
        staff, Offset(0), Offset(3, 16))

    assert testtools.compare(
        new_staff,
        r'''
        \new Staff {
            c'8
            d'16
        }
        '''
        )

    assert select(new_staff).is_well_formed()


def test_componenttools_copy_and_trim_08():
    r'''Start-to-mid clean cut.
    '''

    note = Note("c'4")
    new_note = componenttools.copy_and_trim(
        note, 0, (1, 8))

    assert new_note.lilypond_format == "c'8"
    assert select(new_note).is_well_formed()


def test_componenttools_copy_and_trim_09():
    r'''Start-to-mid jagged cut.
    '''

    note = Note("c'4")
    new_tuplet = componenttools.copy_and_trim(
        note, Offset(0), Offset(1, 12))

    assert testtools.compare(
        new_tuplet,
        r'''
        \times 2/3 {
            c'8
        }
        '''
        )

    assert select(new_tuplet).is_well_formed()


def test_componenttools_copy_and_trim_10():
    r'''Mid-mid jagged cut.
    '''

    note = Note("c'4")
    new_tuplet = componenttools.copy_and_trim(
        note, Offset(1, 12), Offset(2, 12))

    assert testtools.compare(
        new_tuplet,
        r'''
        \times 2/3 {
            c'8
        }
        '''
        )

    assert select(new_tuplet).is_well_formed()


def test_componenttools_copy_and_trim_11():
    r'''Mid-to-stop jagged cut.
    '''

    note = Note("c'4")
    new_tuplet = componenttools.copy_and_trim(
        note, Offset(1, 6), Offset(1, 4))

    assert testtools.compare(
        new_tuplet,
        r'''
        \times 2/3 {
            c'8
        }
        '''
        )

    assert select(new_tuplet).is_well_formed()


def test_componenttools_copy_and_trim_12():
    r'''Start-to-after clean cut.
    '''

    note = Note("c'4")
    new_note = componenttools.copy_and_trim(
        note, Offset(0), Offset(1, 2))

    assert new_note.lilypond_format == "c'4"
    assert select(new_note).is_well_formed()


def test_componenttools_copy_and_trim_13():
    r'''Mid-to-after clean cut.
    '''

    note = Note("c'4")
    new_note = componenttools.copy_and_trim(
        note, Offset(1, 8), Offset(1, 2))

    assert new_note.lilypond_format == "c'8"
    assert select(new_note).is_well_formed()


def test_componenttools_copy_and_trim_14():
    r'''Mid-to-after jagged cut.
    '''

    note = Note("c'4")
    new_tuplet = componenttools.copy_and_trim(
        note, Offset(2, 12), Offset(1, 2))

    assert testtools.compare(
        new_tuplet,
        r'''
        \times 2/3 {
            c'8
        }
        '''
        )

    assert select(new_tuplet).is_well_formed()


def test_componenttools_copy_and_trim_15():
    r'''Before-to-after.
    '''

    note = Note("c'4")
    new_note = componenttools.copy_and_trim(
        note, Offset(-1, 4), Offset(1, 2))

    assert new_note.lilypond_format == "c'4"
    assert select(new_note).is_well_formed()


def test_componenttools_copy_and_trim_16():
    r'''Start-to-mid jagged.
    '''

    note = Note("c'4")
    new_tuplet = componenttools.copy_and_trim(
        note, Offset(0), Offset(5, 24))

    assert testtools.compare(
        new_tuplet,
        r'''
        \times 2/3 {
            c'4 ~
            c'16
        }
        '''
        )

    assert select(new_tuplet).is_well_formed()


def test_componenttools_copy_and_trim_17():
    r'''Start-to-mid jagged.
    '''

    note = Note("c'4")
    new_tuplet = componenttools.copy_and_trim(
        note, Offset(0), Offset(1, 5))

    assert testtools.compare(
        new_tuplet,
        r'''
        \times 4/5 {
            c'4
        }
        '''
        )

    assert select(new_tuplet).is_well_formed()
