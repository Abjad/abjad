# -*- encoding: utf-8 -*-
from abjad import *


def test_Note_add_artificial_harmonic_01():
    r'''Adds a perfect fourth by default.
    '''

    t = Note("c'4")
    t = t.add_artificial_harmonic()
    assert testtools.compare(
        t.lilypond_format,
        "<\n\tc'\n\t\\tweak #'style #'harmonic\n\tf'\n>4"
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

    t = Note("c'4")
    diatonic_interval = pitchtools.MelodicDiatonicInterval('minor', 3)
    t = t.add_artificial_harmonic(diatonic_interval)
    assert testtools.compare(
        t.lilypond_format,
        "<\n\tc'\n\t\\tweak #'style #'harmonic\n\tef'\n>4"
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

    t = Staff([Note(n, (1, 8)) for n in range(8)])
    t[2].add_artificial_harmonic()

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

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\tc'8\n\tcs'8\n\t<\n\t\td'\n\t\t\\tweak #'style #'harmonic\n\t\tg'\n\t>8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
        )
