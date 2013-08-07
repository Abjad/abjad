# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_set_default_accidental_spelling_01():

    staff = Staff([Note(n, (1, 8)) for n in range(12)])

    r'''
    \new Staff {
        c'8
        cs'8
        d'8
        ef'8
        e'8
        f'8
        fs'8
        g'8
        af'8
        a'8
        bf'8
        b'8
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8
            cs'8
            d'8
            ef'8
            e'8
            f'8
            fs'8
            g'8
            af'8
            a'8
            bf'8
            b'8
        }
        '''
        )


def test_pitchtools_set_default_accidental_spelling_02():

    pitchtools.set_default_accidental_spelling('sharps')
    staff = Staff([Note(n, (1, 8)) for n in range(12)])

    r'''
    \new Staff {
        c'8
        cs'8
        d'8
        ds'8
        e'8
        f'8
        fs'8
        g'8
        gs'8
        a'8
        as'8
        b'8
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8
            cs'8
            d'8
            ds'8
            e'8
            f'8
            fs'8
            g'8
            gs'8
            a'8
            as'8
            b'8
        }
        '''
        )

    pitchtools.set_default_accidental_spelling('mixed')


def test_pitchtools_set_default_accidental_spelling_03():

    pitchtools.set_default_accidental_spelling('flats')
    staff = Staff([Note(n, (1, 8)) for n in range(12)])

    r'''
    \new Staff {
        c'8
        df'8
        d'8
        ef'8
        e'8
        f'8
        gf'8
        g'8
        af'8
        a'8
        bf'8
        b'8
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8
            df'8
            d'8
            ef'8
            e'8
            f'8
            gf'8
            g'8
            af'8
            a'8
            bf'8
            b'8
        }
        '''
        )

    pitchtools.set_default_accidental_spelling('mixed')


def test_pitchtools_set_default_accidental_spelling_04():
    r'''Revert back to default mixed spelling.
    '''

    pitchtools.set_default_accidental_spelling('mixed')
    staff = Staff([Note(n, (1, 8)) for n in range(12)])

    r'''
    \new Staff {
        c'8
        cs'8
        d'8
        ef'8
        e'8
        f'8
        fs'8
        g'8
        af'8
        a'8
        bf'8
        b'8
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8
            cs'8
            d'8
            ef'8
            e'8
            f'8
            fs'8
            g'8
            af'8
            a'8
            bf'8
            b'8
        }
        '''
        )
