from abjad import *
from abjad.tools import configurationtools


def test_configurationtools_set_default_accidental_spelling_01():

    t = Staff([Note(n, (1, 8)) for n in range(12)])

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

    assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\taf'8\n\ta'8\n\tbf'8\n\tb'8\n}"


def test_configurationtools_set_default_accidental_spelling_02():

    configurationtools.set_default_accidental_spelling('sharps')
    t = Staff([Note(n, (1, 8)) for n in range(12)])

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

    assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tds'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\tgs'8\n\ta'8\n\tas'8\n\tb'8\n}"


def test_configurationtools_set_default_accidental_spelling_03():

    configurationtools.set_default_accidental_spelling('flats')
    t = Staff([Note(n, (1, 8)) for n in range(12)])

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

    assert t.format == "\\new Staff {\n\tc'8\n\tdf'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tgf'8\n\tg'8\n\taf'8\n\ta'8\n\tbf'8\n\tb'8\n}"


def test_configurationtools_set_default_accidental_spelling_04():
    '''Revert back to default mixed spelling.'''

    configurationtools.set_default_accidental_spelling('mixed')
    t = Staff([Note(n, (1, 8)) for n in range(12)])

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

    assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\taf'8\n\ta'8\n\tbf'8\n\tb'8\n}"
