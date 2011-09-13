from abjad import *


def test_Accidental_semitones_01():

    assert pitchtools.Accidental('ss').semitones == 2
    assert pitchtools.Accidental('tqs').semitones == 1.5
    assert pitchtools.Accidental('s').semitones == 1
    assert pitchtools.Accidental('qs').semitones == 0.5
    assert pitchtools.Accidental('').semitones == 0
    assert pitchtools.Accidental('qf').semitones == -0.5
    assert pitchtools.Accidental('f').semitones == -1
    assert pitchtools.Accidental('tqf').semitones == -1.5
    assert pitchtools.Accidental('ff').semitones == -2
