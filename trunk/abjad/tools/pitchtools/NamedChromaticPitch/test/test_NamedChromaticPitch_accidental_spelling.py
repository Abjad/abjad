from abjad import *


def test_NamedChromaticPitch_accidental_spelling_01():
    '''Accidentals spell mixed with sharps and flats by default.'''

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


def test_NamedChromaticPitch_accidental_spelling_02():
    '''
    Accidentals can spell as all sharps by changing the
    accidental_class attribute on the Abjad NamedChromaticPitch class.
    '''

    pitchtools.NamedChromaticPitch.accidental_spelling = 'sharps'
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

    pitchtools.NamedChromaticPitch.accidental_spelling = 'mixed'


def test_NamedChromaticPitch_accidental_spelling_03():
    '''
    Accidentals can spell all as flats by changing the
    accidental_spelling attribute on the Abjad NamedChromaticPitch class.
    '''

    pitchtools.NamedChromaticPitch.accidental_spelling = 'flats'
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

    pitchtools.NamedChromaticPitch.accidental_spelling = 'mixed'


def test_NamedChromaticPitch_accidental_spelling_04():
    '''
    You can change accidental spelling modes as many times as you
    like in a single interpreter session or script.
    '''

    t = Staff()

    pitchtools.NamedChromaticPitch.accidental_spelling = 'sharps'
    t.extend([Note(n, (1, 8)) for n in range(6)])

    pitchtools.NamedChromaticPitch.accidental_spelling = 'flats'
    t.extend([Note(n, (1, 8)) for n in range(6)])

    r'''
    \new Staff {
        c'8
        cs'8
        d'8
        ds'8
        e'8
        f'8
        c'8
        df'8
        d'8
        ef'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tds'8\n\te'8\n\tf'8\n\tc'8\n\tdf'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n}"

    pitchtools.NamedChromaticPitch.accidental_spelling = 'mixed'
