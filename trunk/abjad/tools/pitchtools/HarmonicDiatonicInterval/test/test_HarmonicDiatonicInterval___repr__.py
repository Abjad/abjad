from abjad import *


def test_HarmonicDiatonicInterval___repr___01():

    interval = pitchtools.HarmonicDiatonicInterval('perfect', 1)
    repr = interval.__repr__()
    assert  repr == "HarmonicDiatonicInterval('P1')"

    interval = pitchtools.HarmonicDiatonicInterval('augmented', 1)
    repr = interval.__repr__()
    assert  repr == "HarmonicDiatonicInterval('aug1')"

    interval = pitchtools.HarmonicDiatonicInterval('minor', 2)
    repr = interval.__repr__()
    assert  repr == "HarmonicDiatonicInterval('m2')"

    interval = pitchtools.HarmonicDiatonicInterval('major', 2)
    repr = interval.__repr__()
    assert  repr == "HarmonicDiatonicInterval('M2')"

    interval = pitchtools.HarmonicDiatonicInterval('minor', 3)
    repr = interval.__repr__()
    assert  repr == "HarmonicDiatonicInterval('m3')"


def test_HarmonicDiatonicInterval___repr___02():

    interval = pitchtools.HarmonicDiatonicInterval('perfect', -1)
    repr = interval.__repr__()
    assert  repr == "HarmonicDiatonicInterval('P1')"

    interval = pitchtools.HarmonicDiatonicInterval('augmented', -1)
    repr = interval.__repr__()
    assert  repr == "HarmonicDiatonicInterval('aug1')"

    interval = pitchtools.HarmonicDiatonicInterval('minor', -2)
    repr = interval.__repr__()
    assert  repr == "HarmonicDiatonicInterval('m2')"

    interval = pitchtools.HarmonicDiatonicInterval('major', -2)
    repr = interval.__repr__()
    assert  repr == "HarmonicDiatonicInterval('M2')"

    interval = pitchtools.HarmonicDiatonicInterval('minor', -3)
    repr = interval.__repr__()
    assert  repr == "HarmonicDiatonicInterval('m3')"
