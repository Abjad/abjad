# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_respell_named_chromatic_pitches_in_expr_with_sharps_01():
    r'''The pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps()
    helper renotates an individual pitch.'''

    namedchromaticpitch = pitchtools.NamedChromaticPitch('df', 4)
    assert pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps(namedchromaticpitch) == \
        pitchtools.NamedChromaticPitch('cs', 4)


def test_pitchtools_respell_named_chromatic_pitches_in_expr_with_sharps_02():
    r'''The pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps()
    helper renotates the pitch of one note.'''

    note = Note(('df', 4), 4)
    pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps(note)
    assert note.written_pitch == pitchtools.NamedChromaticPitch('cs', 4)


def test_pitchtools_respell_named_chromatic_pitches_in_expr_with_sharps_03():
    r'''The pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps()
    helper renotates the pitches of all notes in a chord.'''

    chord = Chord([('df', 4), ('f', 4), ('af', 4)], (1, 4))
    pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps(chord)
    assert chord.written_pitches == (pitchtools.NamedChromaticPitch('cs', 4), pitchtools.NamedChromaticPitch('f', 4), pitchtools.NamedChromaticPitch('gs', 4))


def test_pitchtools_respell_named_chromatic_pitches_in_expr_with_sharps_04():
    r'''The pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps()
    helper renotates all pitches in any arbirary expression.'''

    staff = Staff(notetools.make_repeated_notes(12))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)
    pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps(staff)

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
        staff,
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
