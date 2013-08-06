# -*- encoding: utf-8 -*-
from abjad import *


def test_Chord_divide_01():
    r'''Divide at D4.
    '''

    staff = Staff("<d' ef' e'>4")
    pitch = pitchtools.NamedChromaticPitch('d', 4)
    treble, bass = staff[0].divide(pitch)
    staff.extend([treble, bass])

    r'''
    \new Staff {
        <d' ef' e'>4
        <d' ef' e'>4
        r4
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        "\\new Staff {\n\t<d' ef' e'>4\n\t<d' ef' e'>4\n\tr4\n}"
        )
    assert select(staff).is_well_formed()



def test_Chord_divide_02():
    r'''Divide at Eb4.
    '''

    staff = Staff("<d' ef' e'>4")
    pitch = pitchtools.NamedChromaticPitch('ef', 4)
    treble, bass = staff[0].divide(pitch)
    staff.extend([treble, bass])

    r'''
    \new Staff {
        <d' ef' e'>4
        <ef' e'>4
        d'4
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        "\\new Staff {\n\t<d' ef' e'>4\n\t<ef' e'>4\n\td'4\n}"
        )
    assert select(staff).is_well_formed()


def test_Chord_divide_03():
    r'''Divide at E4.
    '''

    staff = Staff("<d' ef' e'>4")
    pitch = pitchtools.NamedChromaticPitch('e', 4)
    treble, bass = staff[0].divide(pitch)
    staff.extend([treble, bass])

    r'''
    \new Staff {
        <d' ef' e'>4
        e'4
        <d' ef'>4
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        "\\new Staff {\n\t<d' ef' e'>4\n\te'4\n\t<d' ef'>4\n}"
        )
    assert select(staff).is_well_formed()
