# -*- encoding: utf-8 -*-
from abjad import *


def test_iterationtools_iterate_logical_voice_from_component_01():
    r'''Iterate only notes.
    '''

    container_1 = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
    container_1.is_simultaneous = True
    container_1[0].name = 'voice 1'
    container_1[1].name = 'voice 2'

    container_2 = Container([Voice("g'8 a'8"), Voice("b'8 c''8")])
    container_2.is_simultaneous = True
    container_2[0].name = 'voice 1'
    container_2[1].name = 'voice 2'

    staff = Staff([container_1, container_2])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            <<
                \context Voice = "voice 1" {
                    c'8
                    d'8
                }
                \context Voice = "voice 2" {
                    e'8
                    f'8
                }
            >>
            <<
                \context Voice = "voice 1" {
                    g'8
                    a'8
                }
                \context Voice = "voice 2" {
                    b'8
                    c''8
                }
            >>
        }
        '''
        )

    notes = iterationtools.iterate_logical_voice_from_component(
        staff.select_leaves(allow_discontiguous_leaves=True)[-1], 
        Note, 
        reverse=True)
    notes = list(notes)

    voice_2_first_half = staff[0][1]
    voice_2_second_half = staff[1][1]

    assert notes[0] is voice_2_second_half[1]
    assert notes[1] is voice_2_second_half[0]
    assert notes[2] is voice_2_first_half[1]
    assert notes[3] is voice_2_first_half[0]


def test_iterationtools_iterate_logical_voice_from_component_02():
    r'''Iterate all components.
    '''

    container_1 = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
    container_1.is_simultaneous = True
    container_1[0].name = 'voice 1'
    container_1[1].name = 'voice 2'

    container_2 = Container([Voice("g'8 a'8"), Voice("b'8 c''8")])
    container_2.is_simultaneous = True
    container_2[0].name = 'voice 1'
    container_2[1].name = 'voice 2'

    staff = Staff([container_1, container_2])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            <<
                \context Voice = "voice 1" {
                    c'8
                    d'8
                }
                \context Voice = "voice 2" {
                    e'8
                    f'8
                }
            >>
            <<
                \context Voice = "voice 1" {
                    g'8
                    a'8
                }
                \context Voice = "voice 2" {
                    b'8
                    c''8
                }
            >>
        }
        '''
        )

    leaf = staff.select_leaves(allow_discontiguous_leaves=True)[-1]
    components = iterationtools.iterate_logical_voice_from_component(
        leaf, 
        reverse=True,
        )
    components = list(components)

    r'''
    Note(c'', 8)
    Voice{2}
    Note(b', 8)
    Voice{2}
    Note(f', 8)
    Note(e', 8)
    '''

    leaves = staff.select_leaves(allow_discontiguous_leaves=True)
    assert components[0] is leaves[-1]
    assert components[1] is staff[1][1]
    assert components[2] is leaves[-2]
    assert components[3] is staff[0][1]
    assert components[4] is staff[0][1][1]
    assert components[5] is staff[0][1][0]


def test_iterationtools_iterate_logical_voice_from_component_03():

    container_1 = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
    container_1.is_simultaneous = True
    container_1[0].name = 'voice 1'
    container_1[1].name = 'voice 2'

    container_2 = Container([Voice("g'8 a'8"), Voice("b'8 c''8")])
    container_2.is_simultaneous = True
    container_2[0].name = 'voice 1'
    container_2[1].name = 'voice 2'

    staff = Staff([container_1, container_2])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            <<
                \context Voice = "voice 1" {
                    c'8
                    d'8
                }
                \context Voice = "voice 2" {
                    e'8
                    f'8
                }
            >>
            <<
                \context Voice = "voice 1" {
                    g'8
                    a'8
                }
                \context Voice = "voice 2" {
                    b'8
                    c''8
                }
            >>
        }
        '''
        )

    leaves = staff.select_leaves(allow_discontiguous_leaves=True)
    notes = iterationtools.iterate_logical_voice_from_component(
        leaves[0], 
        Note,
        )
    notes = list(notes)

    voice_1_first_half = staff[0][0]
    voice_1_second_half = staff[1][0]

    assert notes[0] is voice_1_first_half[0]
    assert notes[1] is voice_1_first_half[1]
    assert notes[2] is voice_1_second_half[0]
    assert notes[3] is voice_1_second_half[1]


def test_iterationtools_iterate_logical_voice_from_component_04():

    container_1 = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
    container_1.is_simultaneous = True
    container_1[0].name = 'voice 1'
    container_1[1].name = 'voice 2'

    container_2 = Container([Voice("g'8 a'8"), Voice("b'8 c''8")])
    container_2.is_simultaneous = True
    container_2[0].name = 'voice 1'
    container_2[1].name = 'voice 2'

    staff = Staff([container_1, container_2])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            <<
                \context Voice = "voice 1" {
                    c'8
                    d'8
                }
                \context Voice = "voice 2" {
                    e'8
                    f'8
                }
            >>
            <<
                \context Voice = "voice 1" {
                    g'8
                    a'8
                }
                \context Voice = "voice 2" {
                    b'8
                    c''8
                }
            >>
        }
        '''
        )

    leaves = staff.select_leaves(allow_discontiguous_leaves=True)
    leaf = leaves[0]
    components = iterationtools.iterate_logical_voice_from_component(leaf)
    components = list(components)

    r'''
    c'8
    Voice{2}
    d'8
    Voice{2}
    g'8
    a'8
    '''

    assert components[0] is leaves[0]
    assert components[1] is staff[0][0]
    assert components[2] is leaves[1]
    assert components[3] is staff[1][0]
    assert components[4] is staff[1][0][0]
    assert components[5] is staff[1][0][1]
