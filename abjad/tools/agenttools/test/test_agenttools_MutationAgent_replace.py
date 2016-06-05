# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_MutationAgent_replace_01():
    r'''Moves parentage and spanners from two old notes to five new notes.

    Equivalent to staff[1:3] = new_notes.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam_1 = Beam()
    attach(beam_1, staff[:2])
    beam_2 = Beam()
    attach(beam_2, staff[2:])
    crescendo = Crescendo()
    attach(crescendo, staff[:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [ \<
            d'8 ]
            e'8 [
            f'8 ] \!
        }
        '''
        ), format(staff)

    old_notes = staff[1:3]
    new_notes = 5 * Note("c''16")
    mutate(old_notes).replace(new_notes)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [ ] \<
            c''16
            c''16
            c''16
            c''16
            c''16
            f'8 \! [ ]
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_replace_02():
    r'''Moves parentage and spanners from one old note to five new notes.

    Equivalent to staff[:1] = new_notes.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam_1 = Beam()
    attach(beam_1, staff[:2])
    beam_2 = Beam()
    attach(beam_2, staff[2:])
    crescendo = Crescendo()
    attach(crescendo, staff[:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [ \<
            d'8 ]
            e'8 [
            f'8 ] \!
        }
        '''
        ), format(staff)

    old_notes = staff[:1]
    new_notes = 5 * Note("c''16")
    mutate(old_notes).replace(new_notes)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c''16 [ \<
            c''16
            c''16
            c''16
            c''16
            d'8 ]
            e'8 [
            f'8 ] \!
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_replace_03():
    r'''Moves parentage and spanners from two old notes to five new notes.

    Equivalent to staff[:2] = new_notes.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam_1 = Beam()
    attach(beam_1, staff[:2])
    beam_2 = Beam()
    attach(beam_2, staff[2:])
    crescendo = Crescendo()
    attach(crescendo, staff[:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [ \<
            d'8 ]
            e'8 [
            f'8 ] \!
        }
        '''
        ), format(staff)

    old_notes = staff[:2]
    new_notes = 5 * Note("c''16")
    mutate(old_notes).replace(new_notes)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c''16 [ \<
            c''16
            c''16
            c''16
            c''16 ]
            e'8 [
            f'8 ] \!
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_replace_04():
    r'''Moves parentage and spanners from three old notes to five new notes.

    "Equivalent to staff[:3] = new_notes."
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam_1 = Beam()
    attach(beam_1, staff[:2])
    beam_2 = Beam()
    attach(beam_2, staff[2:])
    crescendo = Crescendo()
    attach(crescendo, staff[:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [ \<
            d'8 ]
            e'8 [
            f'8 ] \!
        }
        '''
        ), format(staff)

    old_notes = staff[:3]
    new_notes = 5 * Note("c''16")
    mutate(old_notes).replace(new_notes)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c''16 \<
            c''16
            c''16
            c''16
            c''16
            f'8 \! [ ]
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_replace_05():
    r'''Moves parentage and spanners from four old notes to five new notes.

    Equivalent to staff[:] = new_notes.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam_1 = Beam()
    attach(beam_1, staff[:2])
    beam_2 = Beam()
    attach(beam_2, staff[2:])
    crescendo = Crescendo()
    attach(crescendo, staff[:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [ \<
            d'8 ]
            e'8 [
            f'8 ] \!
        }
        '''
        ), format(staff)

    old_notes = staff[:]
    new_notes = 5 * Note("c''16")
    mutate(old_notes).replace(new_notes)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c''16 \<
            c''16
            c''16
            c''16
            c''16 \!
        }
        '''
        ), format(staff)

    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_replace_06():
    r'''Moves parentage and spanners from container to children of container.

    Replaces container with contents of container.

    Effectively removes container from score.

    Equivalent to staff[:1] = staff[0][:].
    '''

    staff = Staff([Voice("c'8 d'8 e'8 f'8")])
    beam = Beam()
    attach(beam, staff[0][:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \new Voice {
                c'8 [
                d'8
                e'8
                f'8 ]
            }
        }
        '''
        ), format(staff)

    voice_selection = staff[:1]
    voice = voice_selection[0]
    old_components = mutate(voice_selection).replace(staff[0][:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        ), format(staff)

    assert not voice
    assert inspect_(staff).is_well_formed()
