# -*- encoding: utf-8 -*-
from abjad import *


def test_Note_add_artificial_harmonic_01():
    r'''Adds a perfect fourth by default.
    '''

    note = Note("c'4")
    note = note.add_artificial_harmonic()
    assert testtools.compare(
        note,
        r'''
        <
            c'
            \tweak #'style #'harmonic
            f'
        >4
        '''
        )

    r'''
    <
        c'
        \tweak #'style #'harmonic
        f'
    >4
    '''


def test_Note_add_artificial_harmonic_02():
    r'''Specify other diatonic intervals explicitly.
    '''

    note = Note("c'4")
    named_interval = pitchtools.NamedInterval('minor', 3)
    note = note.add_artificial_harmonic(named_interval)
    assert testtools.compare(
        note,
        r'''
        <
            c'
            \tweak #'style #'harmonic
            ef'
        >4
        '''
        )

    r'''
    <
        c'
        \tweak #'style #'harmonic
        ef'
    >4
    '''


def test_Note_add_artificial_harmonic_03():
    r'''Works in staves.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    staff[2].add_artificial_harmonic()

    r'''
    \new Staff {
        c'8
        cs'8
        <
            d'
            \tweak #'style #'harmonic
            g'
        >8
        ef'8
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            cs'8
            <
                d'
                \tweak #'style #'harmonic
                g'
            >8
            ef'8
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )
