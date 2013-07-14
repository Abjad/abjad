from abjad import *


def test_chordtools_divide_chord_by_diatonic_pitch_number_01():
    '''Divide at D4.
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

    assert staff.lilypond_format == "\\new Staff {\n\t<d' ef' e'>4\n\t<d' ef' e'>4\n\tr4\n}"
    assert wellformednesstools.is_well_formed_component(staff)



def test_chordtools_divide_chord_by_diatonic_pitch_number_02():
    '''Divide at Eb4.
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

    assert staff.lilypond_format == "\\new Staff {\n\t<d' ef' e'>4\n\t<ef' e'>4\n\td'4\n}"
    assert wellformednesstools.is_well_formed_component(staff)


def test_chordtools_divide_chord_by_diatonic_pitch_number_03():
    '''Divide at E4.
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

    assert staff.lilypond_format == "\\new Staff {\n\t<d' ef' e'>4\n\te'4\n\t<d' ef'>4\n}"
    assert wellformednesstools.is_well_formed_component(staff)
