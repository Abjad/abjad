from abjad.tools.pitchtools import NamedChromaticPitch
from abjad.tools.pitchtools import make_n_middle_c_centered_pitches


def test_pitchtools_make_n_middle_c_centered_pitches_01():
    pitches = make_n_middle_c_centered_pitches(0)
    assert len(pitches) == 0


def test_pitchtools_make_n_middle_c_centered_pitches_02():
    pitches = make_n_middle_c_centered_pitches(2)
    assert pitches == [NamedChromaticPitch('b'), NamedChromaticPitch("d'")]


def test_pitchtools_make_n_middle_c_centered_pitches_03():
    pitches = make_n_middle_c_centered_pitches(-2)
    assert pitches == [NamedChromaticPitch("d'"), NamedChromaticPitch('b')]


def test_pitchtools_make_n_middle_c_centered_pitches_04():
    pitches = make_n_middle_c_centered_pitches(3)
    assert pitches == [NamedChromaticPitch('a'), NamedChromaticPitch("c'"), NamedChromaticPitch("e'")]
