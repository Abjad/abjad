# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_MutationAgent_respell_with_flats_01():

    note = Note(('cs', 4), 4)
    mutate(note).respell_with_flats()

    assert note.written_pitch == NamedPitch('df', 4)


def test_agenttools_MutationAgent_respell_with_flats_02():

    chord = Chord([('cs', 4), ('f', 4), ('as', 4)], (1, 4))
    mutate(chord).respell_with_flats()

    assert chord.written_pitches == (
        NamedPitch('df', 4),
        NamedPitch('f', 4),
        NamedPitch('bf', 4),
        )


def test_agenttools_MutationAgent_respell_with_flats_03():

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8 af'8 a'8 bf'8 b'")
    mutate(staff).respell_with_flats()

    assert format(staff) == stringtools.normalize(
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
