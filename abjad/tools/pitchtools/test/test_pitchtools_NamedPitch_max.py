# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitch_max_01():
    r'''Built-in max() works when __gt__ is defined.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    written_pitches = [note.written_pitch for note in staff]
    max_pitch = max(written_pitches)

    assert max_pitch == NamedPitch('f', 4)
