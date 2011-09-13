from abjad import *


def test_NamedChromaticPitch_max_01():
    '''Built-in max() works when __gt__ is defined.'''

    t = Staff("c'8 d'8 e'8 f'8")
    written_pitches = [note.written_pitch for note in t]
    max_pitch = max(written_pitches)

    assert max_pitch == pitchtools.NamedChromaticPitch('f', 4)
