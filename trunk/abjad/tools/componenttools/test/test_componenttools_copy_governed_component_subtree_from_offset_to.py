# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_copy_governed_component_subtree_from_offset_to_01():
    r'''Container.
    '''

    container = Container("c'8 d'8 e'8")
    new_container = componenttools.copy_governed_component_subtree_from_offset_to(
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


def test_componenttools_copy_governed_component_subtree_from_offset_to_02():
    r'''Container with rest.
    '''

    container = Container("c'8 r8 e'8")
    new_container = componenttools.copy_governed_component_subtree_from_offset_to(
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


def test_componenttools_copy_governed_component_subtree_from_offset_to_03():
    r'''Copy measure.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")
    new_measure = componenttools.copy_governed_component_subtree_from_offset_to(
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


def test_componenttools_copy_governed_component_subtree_from_offset_to_04():
    r'''Fixed-duration tuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(1, 4), "c'8 d'8 e'8")
    new_tuplet = componenttools.copy_governed_component_subtree_from_offset_to(
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


def test_componenttools_copy_governed_component_subtree_from_offset_to_05():
    r'''Tuplet.
    '''

    tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
    new_tuplet = componenttools.copy_governed_component_subtree_from_offset_to(
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


def test_componenttools_copy_governed_component_subtree_from_offset_to_06():
    r'''Voice.
    '''

    voice = Voice("c'8 d'8 e'8")
    new_voice = componenttools.copy_governed_component_subtree_from_offset_to(
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


def test_componenttools_copy_governed_component_subtree_from_offset_to_07():
    r'''Staff.
    '''

    staff = Staff("c'8 d'8 e'8")
    new_staff = componenttools.copy_governed_component_subtree_from_offset_to(
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


def test_componenttools_copy_governed_component_subtree_from_offset_to_08():
    r'''Start-to-mid clean cut.
    '''

    note = Note("c'4")
    new_note = componenttools.copy_governed_component_subtree_from_offset_to(
        note, 0, (1, 8))

    assert new_note.lilypond_format == "c'8"
    assert select(new_note).is_well_formed()


def test_componenttools_copy_governed_component_subtree_from_offset_to_09():
    r'''Start-to-mid jagged cut.
    '''

    note = Note("c'4")
    new_note = componenttools.copy_governed_component_subtree_from_offset_to(
        note, Offset(0), Offset(1, 12))
    new_tuplet = more(new_note).select_parentage().parent

    assert testtools.compare(
        new_tuplet,
        r'''
        \times 2/3 {
            c'8
        }
        '''
        )

    assert select(new_tuplet).is_well_formed()


def test_componenttools_copy_governed_component_subtree_from_offset_to_10():
    r'''Mid-mid jagged cut.
    '''

    note = Note("c'4")
    new_note = componenttools.copy_governed_component_subtree_from_offset_to(
        note, Offset(1, 12), Offset(2, 12))
    new_tuplet = more(new_note).select_parentage().parent

    assert testtools.compare(
        new_tuplet,
        r'''
        \times 2/3 {
            c'8
        }
        '''
        )

    assert select(new_tuplet).is_well_formed()


def test_componenttools_copy_governed_component_subtree_from_offset_to_11():
    r'''Mid-to-stop jagged cut.
    '''

    note = Note("c'4")
    new_note = componenttools.copy_governed_component_subtree_from_offset_to(
        note, Offset(1, 6), Offset(1, 4))
    new_tuplet = more(new_note).select_parentage().parent

    assert testtools.compare(
        new_tuplet,
        r'''
        \times 2/3 {
            c'8
        }
        '''
        )

    assert select(new_tuplet).is_well_formed()


def test_componenttools_copy_governed_component_subtree_from_offset_to_12():
    r'''Start-to-after clean cut.
    '''

    note = Note("c'4")
    new_note = componenttools.copy_governed_component_subtree_from_offset_to(
        note, Offset(0), Offset(1, 2))

    assert new_note.lilypond_format == "c'4"
    assert select(new_note).is_well_formed()


def test_componenttools_copy_governed_component_subtree_from_offset_to_13():
    r'''Mid-to-after clean cut.
    '''

    note = Note("c'4")
    new_note = componenttools.copy_governed_component_subtree_from_offset_to(
        note, Offset(1, 8), Offset(1, 2))

    assert new_note.lilypond_format == "c'8"
    assert select(new_note).is_well_formed()


def test_componenttools_copy_governed_component_subtree_from_offset_to_14():
    r'''Mid-to-after jagged cut.
    '''

    note = Note("c'4")
    new_note = componenttools.copy_governed_component_subtree_from_offset_to(
        note, Offset(2, 12), Offset(1, 2))
    new_tuplet = more(new_note).select_parentage().parent

    assert testtools.compare(
        new_tuplet,
        r'''
        \times 2/3 {
            c'8
        }
        '''
        )

    assert select(new_tuplet).is_well_formed()


def test_componenttools_copy_governed_component_subtree_from_offset_to_15():
    r'''Before-to-after.
    '''

    note = Note("c'4")
    new_note = componenttools.copy_governed_component_subtree_from_offset_to(
        note, Offset(-1, 4), Offset(1, 2))

    assert new_note.lilypond_format == "c'4"
    assert select(new_note).is_well_formed()


def test_componenttools_copy_governed_component_subtree_from_offset_to_16():
    r'''Start-to-mid jagged.
    '''

    note = Note("c'4")
    new_note = componenttools.copy_governed_component_subtree_from_offset_to(
        note, Offset(0), Offset(5, 24))
    new_tuplet = more(new_note).select_parentage().parent

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


def test_componenttools_copy_governed_component_subtree_from_offset_to_17():
    r'''Start-to-mid jagged.
    '''

    note = Note("c'4")
    new_note = componenttools.copy_governed_component_subtree_from_offset_to(
        note, Offset(0), Offset(1, 5))
    new_tuplet = more(new_note).select_parentage().parent

    assert testtools.compare(
        new_tuplet,
        r'''
        \times 4/5 {
            c'4
        }
        '''
        )

    assert select(new_tuplet).is_well_formed()
