# -*- coding: utf-8 -*-
import pytest
from abjad import *
Selection = selectiontools.Selection



def test_selectiontools_Selection__all_are_contiguous_components_in_same_logical_voice_01():
    r'''Components that start at the same moment are bad.
    Even if components are all part of the same logical voice.
    '''

    voice = Voice(r'''
        {
            c'8
            d'8
        }
        \new Voice {
            e'8
            f'8
        }
        {
            g'8
            a'8
        }
        ''')

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        \new Voice {
            e'8
            f'8
        }
        {
            g'8
            a'8
        }
    }
    '''

    assert not Selection._all_are_contiguous_components_in_same_logical_voice(
        [voice, voice[0]])
    assert not Selection._all_are_contiguous_components_in_same_logical_voice(
        voice[0:1] + voice[0][:])
    assert not Selection._all_are_contiguous_components_in_same_logical_voice(
        voice[-1:] + voice[-1][:])


def test_selectiontools_Selection__all_are_contiguous_components_in_same_logical_voice_02():
    r'''True for strictly contiguous leaves in same staff.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    assert Selection._all_are_contiguous_components_in_same_logical_voice(staff[:])


def test_selectiontools_Selection__all_are_contiguous_components_in_same_logical_voice_03():
    r'''True for orphan components when allow_orphans is True.
        False for orphan components when allow_orphans is False.'''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    assert Selection._all_are_contiguous_components_in_same_logical_voice(notes)
    assert not Selection._all_are_contiguous_components_in_same_logical_voice(notes, allow_orphans=False)


def test_selectiontools_Selection__all_are_contiguous_components_in_same_logical_voice_04():
    r'''False for time reordered leaves in staff.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    assert not Selection._all_are_contiguous_components_in_same_logical_voice(staff[2:] + staff[:2])


def test_selectiontools_Selection__all_are_contiguous_components_in_same_logical_voice_05():
    r'''True for unincorporated component.
    '''

    assert Selection._all_are_contiguous_components_in_same_logical_voice([Staff("c'8 d'8 e'8 f'8")])


def test_selectiontools_Selection__all_are_contiguous_components_in_same_logical_voice_06():
    r'''True for empty list.
    '''

    assert Selection._all_are_contiguous_components_in_same_logical_voice([])


def test_selectiontools_Selection__all_are_contiguous_components_in_same_logical_voice_07():
    r'''False when components belonging to same logical voice are ommitted.
    '''

    voice = Voice("c'8 d'8 e'8 f'8 g'8 a'8")
    beam = Beam()
    attach(beam, voice[:])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8
            g'8
            a'8 ]
        }
        '''
        )

    assert not Selection._all_are_contiguous_components_in_same_logical_voice(
        voice[:2] + voice[-2:])


def test_selectiontools_Selection__all_are_contiguous_components_in_same_logical_voice_08():
    r'''False when components belonging to same logical voice are ommitted.
    '''

    voice = Voice(r'''
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8
        }
        {
            g'8
            a'8 ]
        }
        ''')

    assert not Selection._all_are_contiguous_components_in_same_logical_voice(voice[:1] + voice[-1:])
