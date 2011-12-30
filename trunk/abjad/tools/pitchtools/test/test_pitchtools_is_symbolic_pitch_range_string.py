from abjad import *


def test_pitchtools_is_symbolic_pitch_range_string_01():

    assert pitchtools.is_symbolic_pitch_range_string('[A#0, Cb~8]')
    assert pitchtools.is_symbolic_pitch_range_string("(A#+0, cs'')")
    assert pitchtools.is_symbolic_pitch_range_string('[c, a)')
    assert pitchtools.is_symbolic_pitch_range_string('(b,,, ctqs]')


def test_pitchtools_is_symbolic_pitch_range_string_02():

    assert not pitchtools.is_symbolic_pitch_range_string('')
    assert not pitchtools.is_symbolic_pitch_range_string('foo')
    assert not pitchtools.is_symbolic_pitch_range_string(True)
    assert not pitchtools.is_symbolic_pitch_range_string(7)
