# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_set_ascending_named_diatonic_pitches_on_tie_chains_in_expr_01():
    r'''Diatonicize notes in staff.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )


def test_pitchtools_set_ascending_named_diatonic_pitches_on_tie_chains_in_expr_02():
    r'''Diatonicize tie chains in staff.
    '''

    staff = Staff(notetools.make_notes(0, [(5, 32)] * 4))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    r'''
    \new Staff {
        c'8 ~
        c'32
        d'8 ~
        d'32
        e'8 ~
        e'32
        f'8 ~
        f'32
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8 ~
            c'32
            d'8 ~
            d'32
            e'8 ~
            e'32
            f'8 ~
            f'32
        }
        '''
        )


def test_pitchtools_set_ascending_named_diatonic_pitches_on_tie_chains_in_expr_03():
    r'''Diatonicize tie chains in staff according to key signature.
    '''

    staff = Staff(notetools.make_notes(0, [(5, 32)] * 4))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff, contexttools.KeySignatureMark('fs', 'major'))

    r'''
    \new Staff {
        fs'8 ~
        fs'32
        gs'8 ~
        gs'32
        as'8 ~
        as'32
        b'8 ~
        b'32
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            fs'8 ~
            fs'32
            gs'8 ~
            gs'32
            as'8 ~
            as'32
            b'8 ~
            b'32
        }
        '''
        )
