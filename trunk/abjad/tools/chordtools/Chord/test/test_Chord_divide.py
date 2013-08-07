# -*- encoding: utf-8 -*-
from abjad import *


def test_Chord_divide_01():
    r'''Divide chord at D4.
    '''

    staff = Staff("<d' ef' e'>4")
    pitch = pitchtools.NamedChromaticPitch('D4')
    treble, bass = staff[0].divide(pitch)
    staff.extend([treble, bass])

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            <d' ef' e'>4
            <d' ef' e'>4
            r4
        }
        '''
        )

    assert select(staff).is_well_formed()


def test_Chord_divide_02():
    r'''Divide chord at Eb4.
    '''

    staff = Staff("<d' ef' e'>4")
    pitch = pitchtools.NamedChromaticPitch('Eb4')
    treble, bass = staff[0].divide(pitch)
    staff.extend([treble, bass])

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            <d' ef' e'>4
            <ef' e'>4
            d'4
        }
        '''
        )

    assert select(staff).is_well_formed()


def test_Chord_divide_03():
    r'''Divide chord at E4.
    '''

    staff = Staff("<d' ef' e'>4")
    pitch = pitchtools.NamedChromaticPitch('E4')
    treble, bass = staff[0].divide(pitch)
    staff.extend([treble, bass])

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            <d' ef' e'>4
            e'4
            <d' ef'>4
        }
        '''
        )

    assert select(staff).is_well_formed()
