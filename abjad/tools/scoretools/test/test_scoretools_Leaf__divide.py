# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Leaf__divide_01():
    r'''Divide chord at D4.
    '''

    staff = Staff("<d' ef' e'>4")
    pitch = NamedPitch('D4')
    treble, bass = staff[0]._divide(pitch)
    staff.extend([treble, bass])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            <d' ef' e'>4
            <d' ef' e'>4
            r4
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_scoretools_Leaf__divide_02():
    r'''Divide chord at Eb4.
    '''

    staff = Staff("<d' ef' e'>4")
    pitch = NamedPitch('Eb4')
    treble, bass = staff[0]._divide(pitch)
    staff.extend([treble, bass])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            <d' ef' e'>4
            <ef' e'>4
            d'4
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_scoretools_Leaf__divide_03():
    r'''Divide chord at E4.
    '''

    staff = Staff("<d' ef' e'>4")
    pitch = NamedPitch('E4')
    treble, bass = staff[0]._divide(pitch)
    staff.extend([treble, bass])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            <d' ef' e'>4
            e'4
            <d' ef'>4
        }
        '''
        )

    assert inspect_(staff).is_well_formed()
