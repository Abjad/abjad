# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_IterationAgent_by_logical_voice_from_component_01():
    r'''Iterates only notes.
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
    leaves = list(iterate(staff).by_leaf())

    assert format(staff) == stringtools.normalize(
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

    component = leaves[-1]
    notes = iterate(component).by_logical_voice_from_component(
        Note, reverse=True)
    notes = list(notes)

    voice_2_first_half = staff[0][1]
    voice_2_second_half = staff[1][1]

    assert notes[0] is voice_2_second_half[1]
    assert notes[1] is voice_2_second_half[0]
    assert notes[2] is voice_2_first_half[1]
    assert notes[3] is voice_2_first_half[0]


def test_agenttools_IterationAgent_by_logical_voice_from_component_02():
    r'''Iterates all components.
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
    leaves = list(iterate(staff).by_leaf())

    assert format(staff) == stringtools.normalize(
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

    leaf = leaves[-1]
    components = iterate(leaf).by_logical_voice_from_component(reverse=True)
    components = list(components)

    r'''
    Note(c'', 8)
    Voice{2}
    Note(b', 8)
    Voice{2}
    Note(f', 8)
    Note(e', 8)
    '''

    assert components[0] is leaves[-1]
    assert components[1] is staff[1][1]
    assert components[2] is leaves[-2]
    assert components[3] is staff[0][1]
    assert components[4] is staff[0][1][1]
    assert components[5] is staff[0][1][0]


def test_agenttools_IterationAgent_by_logical_voice_from_component_03():

    container_1 = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
    container_1.is_simultaneous = True
    container_1[0].name = 'voice 1'
    container_1[1].name = 'voice 2'

    container_2 = Container([Voice("g'8 a'8"), Voice("b'8 c''8")])
    container_2.is_simultaneous = True
    container_2[0].name = 'voice 1'
    container_2[1].name = 'voice 2'

    staff = Staff([container_1, container_2])
    leaves = list(iterate(staff).by_leaf())

    assert format(staff) == stringtools.normalize(
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

    leaf = leaves[0]
    notes = iterate(leaf).by_logical_voice_from_component(Note)
    notes = list(notes)

    voice_1_first_half = staff[0][0]
    voice_1_second_half = staff[1][0]

    assert notes[0] is voice_1_first_half[0]
    assert notes[1] is voice_1_first_half[1]
    assert notes[2] is voice_1_second_half[0]
    assert notes[3] is voice_1_second_half[1]


def test_agenttools_IterationAgent_by_logical_voice_from_component_04():

    container_1 = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
    container_1.is_simultaneous = True
    container_1[0].name = 'voice 1'
    container_1[1].name = 'voice 2'

    container_2 = Container([Voice("g'8 a'8"), Voice("b'8 c''8")])
    container_2.is_simultaneous = True
    container_2[0].name = 'voice 1'
    container_2[1].name = 'voice 2'

    staff = Staff([container_1, container_2])
    leaves = list(iterate(staff).by_leaf())

    assert format(staff) == stringtools.normalize(
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

    leaf = leaves[0]
    components = iterate(leaf).by_logical_voice_from_component()
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