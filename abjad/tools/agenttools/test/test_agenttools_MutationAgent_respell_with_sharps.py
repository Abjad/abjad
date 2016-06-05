# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_MutationAgent_respell_with_sharps_01():

    note = Note(('df', 4), 4)
    mutate(note).respell_with_sharps()

    assert note.written_pitch == NamedPitch('cs', 4)


def test_agenttools_MutationAgent_respell_with_sharps_02():

    chord = Chord([('df', 4), ('f', 4), ('af', 4)], (1, 4))
    mutate(chord).respell_with_sharps()

    assert chord.written_pitches == (
        NamedPitch('cs', 4),
        NamedPitch('f', 4),
        NamedPitch('gs', 4),
        )


def test_agenttools_MutationAgent_respell_with_sharps_03():

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8 af'8 a'8 bf'8 b'")
    mutate(staff).respell_with_sharps()

    assert format(staff) == stringtools.normalize(
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
