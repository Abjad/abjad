from abjad import *


def test_MelodicDiatonicInterval___repr___01():

    interval = pitchtools.MelodicDiatonicInterval('perfect', 1)
    repr = interval.__repr__()
    assert  repr == "MelodicDiatonicInterval('P1')"

    interval = pitchtools.MelodicDiatonicInterval('augmented', 1)
    repr = interval.__repr__()
    assert  repr == "MelodicDiatonicInterval('+aug1')"

    interval = pitchtools.MelodicDiatonicInterval('minor', 2)
    repr = interval.__repr__()
    assert  repr == "MelodicDiatonicInterval('+m2')"

    interval = pitchtools.MelodicDiatonicInterval('major', 2)
    repr = interval.__repr__()
    assert  repr == "MelodicDiatonicInterval('+M2')"

    interval = pitchtools.MelodicDiatonicInterval('minor', 3)
    repr = interval.__repr__()
    assert  repr == "MelodicDiatonicInterval('+m3')"


def test_MelodicDiatonicInterval___repr___02():

    interval = pitchtools.MelodicDiatonicInterval('perfect', -1)
    repr = interval.__repr__()
    assert  repr == "MelodicDiatonicInterval('P1')"

    interval = pitchtools.MelodicDiatonicInterval('augmented', -1)
    repr = interval.__repr__()
    assert  repr == "MelodicDiatonicInterval('-aug1')"

    interval = pitchtools.MelodicDiatonicInterval('minor', -2)
    repr = interval.__repr__()
    assert  repr == "MelodicDiatonicInterval('-m2')"

    interval = pitchtools.MelodicDiatonicInterval('major', -2)
    repr = interval.__repr__()
    assert  repr == "MelodicDiatonicInterval('-M2')"

    interval = pitchtools.MelodicDiatonicInterval('minor', -3)
    repr = interval.__repr__()
    assert  repr == "MelodicDiatonicInterval('-m3')"
