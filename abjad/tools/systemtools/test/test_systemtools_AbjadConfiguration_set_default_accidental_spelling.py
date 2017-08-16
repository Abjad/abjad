import abjad
from abjad.tools import systemtools


def test_systemtools_AbjadConfiguration_set_default_accidental_spelling_01():

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(12)])

    assert format(staff) == abjad.String.normalize(
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


def test_systemtools_AbjadConfiguration_set_default_accidental_spelling_02():

    abjad.abjad_configuration.set_default_accidental_spelling('sharps')
    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(12)])

    assert format(staff) == abjad.String.normalize(
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

    abjad.abjad_configuration.set_default_accidental_spelling('mixed')


def test_systemtools_AbjadConfiguration_set_default_accidental_spelling_03():

    abjad.abjad_configuration.set_default_accidental_spelling('flats')
    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(12)])

    assert format(staff) == abjad.String.normalize(
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

    abjad.abjad_configuration.set_default_accidental_spelling('mixed')


def test_systemtools_AbjadConfiguration_set_default_accidental_spelling_04():
    r'''Revert back to default mixed spelling.
    '''

    abjad.abjad_configuration.set_default_accidental_spelling('mixed')
    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(12)])

    assert format(staff) == abjad.String.normalize(
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
