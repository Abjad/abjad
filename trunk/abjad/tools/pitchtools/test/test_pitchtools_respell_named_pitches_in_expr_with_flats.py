# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_respell_named_pitches_in_expr_with_flats_01():
    r'''The pitchtools.respell_named_pitches_in_expr_with_flats()
    helper renotates an individual pitch.'''

    namedchromaticpitch = pitchtools.NamedPitch('cs', 4)
    assert pitchtools.respell_named_pitches_in_expr_with_flats(namedchromaticpitch) == pitchtools.NamedPitch(
        'df', 4)


def test_pitchtools_respell_named_pitches_in_expr_with_flats_02():
    r'''The pitchtools.respell_named_pitches_in_expr_with_flats()
    helper renotates the pitch of one note.'''

    note = Note(('cs', 4), 4)
    pitchtools.respell_named_pitches_in_expr_with_flats(note)
    assert note.written_pitch == pitchtools.NamedPitch('df', 4)


def test_pitchtools_respell_named_pitches_in_expr_with_flats_03():
    r'''The pitchtools.respell_named_pitches_in_expr_with_flats()
    helper renotates the pitches of all notes in a chord.'''
    chord = Chord([('cs', 4), ('f', 4), ('as', 4)], (1, 4))

    pitchtools.respell_named_pitches_in_expr_with_flats(chord)
    assert chord.written_pitches == (pitchtools.NamedPitch('df', 4), pitchtools.NamedPitch('f', 4), pitchtools.NamedPitch('bf', 4))


def test_pitchtools_respell_named_pitches_in_expr_with_flats_04():
    r'''The pitchtools.respell_named_pitches_in_expr_with_flats()
    helper renotates all pitches in any arbirary expression.'''

    staff = Staff([Note(n, (1, 8)) for n in range(12, 0, -1)])
    pitchtools.respell_named_pitches_in_expr_with_flats(staff)

    r'''
    \new Staff {
        c''8
        b'8
        bf'8
        a'8
        af'8
        g'8
        gf'8
        f'8
        e'8
        ef'8
        d'8
        df'8
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c''8
            b'8
            bf'8
            a'8
            af'8
            g'8
            gf'8
            f'8
            e'8
            ef'8
            d'8
            df'8
        }
        '''
        )
