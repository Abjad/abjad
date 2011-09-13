from abjad import *


def test_NamedChromaticPitch_numbered_diatonic_pitch_01():
    '''Pitches referentially equal.
    '''

    p1 = pitchtools.NamedChromaticPitch('fs', 4)

    assert      p1.numbered_diatonic_pitch == p1.numbered_diatonic_pitch
    assert not p1.numbered_diatonic_pitch != p1.numbered_diatonic_pitch
    assert not p1.numbered_diatonic_pitch >  p1.numbered_diatonic_pitch
    assert      p1.numbered_diatonic_pitch >= p1.numbered_diatonic_pitch
    assert not p1.numbered_diatonic_pitch <  p1.numbered_diatonic_pitch
    assert      p1.numbered_diatonic_pitch <= p1.numbered_diatonic_pitch


def test_NamedChromaticPitch_numbered_diatonic_pitch_02():
    '''Pitches by name, accidental and octave.
    '''

    p1, p2 = pitchtools.NamedChromaticPitch('fs', 4), pitchtools.NamedChromaticPitch('fs', 4)

    assert      p1.numbered_diatonic_pitch == p2.numbered_diatonic_pitch
    assert not p1.numbered_diatonic_pitch != p2.numbered_diatonic_pitch
    assert not p1.numbered_diatonic_pitch >  p2.numbered_diatonic_pitch
    assert      p1.numbered_diatonic_pitch >= p2.numbered_diatonic_pitch
    assert not p1.numbered_diatonic_pitch <  p2.numbered_diatonic_pitch
    assert      p1.numbered_diatonic_pitch <= p2.numbered_diatonic_pitch


def test_NamedChromaticPitch_numbered_diatonic_pitch_03():
    '''Pitches enharmonically equal.
    '''

    p1, p2 = pitchtools.NamedChromaticPitch('fs', 4), pitchtools.NamedChromaticPitch('gf', 4)

    assert not p1.numbered_diatonic_pitch == p2.numbered_diatonic_pitch
    assert      p1.numbered_diatonic_pitch != p2.numbered_diatonic_pitch
    assert not p1.numbered_diatonic_pitch >  p2.numbered_diatonic_pitch
    assert not p1.numbered_diatonic_pitch >= p2.numbered_diatonic_pitch
    assert      p1.numbered_diatonic_pitch <  p2.numbered_diatonic_pitch
    assert      p1.numbered_diatonic_pitch <= p2.numbered_diatonic_pitch


def test_NamedChromaticPitch_numbered_diatonic_pitch_04():
    '''Pitches manifestly different.
    '''

    p1, p2 = pitchtools.NamedChromaticPitch('f', 4), pitchtools.NamedChromaticPitch('g', 4)

    assert not p1.numbered_diatonic_pitch == p2.numbered_diatonic_pitch
    assert      p1.numbered_diatonic_pitch != p2.numbered_diatonic_pitch
    assert not p1.numbered_diatonic_pitch >  p2.numbered_diatonic_pitch
    assert not p1.numbered_diatonic_pitch >= p2.numbered_diatonic_pitch
    assert      p1.numbered_diatonic_pitch <  p2.numbered_diatonic_pitch
    assert      p1.numbered_diatonic_pitch <= p2.numbered_diatonic_pitch


def test_NamedChromaticPitch_numbered_diatonic_pitch_05():
    '''Pitches typographically crossed.
    '''

    p1, p2 = pitchtools.NamedChromaticPitch('fss', 4), pitchtools.NamedChromaticPitch('gff', 4)

    assert not p1.numbered_diatonic_pitch == p2.numbered_diatonic_pitch
    assert      p1.numbered_diatonic_pitch != p2.numbered_diatonic_pitch
    assert not p1.numbered_diatonic_pitch >  p2.numbered_diatonic_pitch
    assert not p1.numbered_diatonic_pitch >= p2.numbered_diatonic_pitch
    assert      p1.numbered_diatonic_pitch <  p2.numbered_diatonic_pitch
    assert      p1.numbered_diatonic_pitch <= p2.numbered_diatonic_pitch
