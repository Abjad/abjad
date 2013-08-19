# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicInterval___repr___01():

    interval = pitchtools.NamedHarmonicInterval('perfect', 1)
    repr = interval.__repr__()
    assert  repr == "NamedHarmonicInterval('P1')"

    interval = pitchtools.NamedHarmonicInterval('augmented', 1)
    repr = interval.__repr__()
    assert  repr == "NamedHarmonicInterval('aug1')"

    interval = pitchtools.NamedHarmonicInterval('minor', 2)
    repr = interval.__repr__()
    assert  repr == "NamedHarmonicInterval('m2')"

    interval = pitchtools.NamedHarmonicInterval('major', 2)
    repr = interval.__repr__()
    assert  repr == "NamedHarmonicInterval('M2')"

    interval = pitchtools.NamedHarmonicInterval('minor', 3)
    repr = interval.__repr__()
    assert  repr == "NamedHarmonicInterval('m3')"


def test_NamedHarmonicInterval___repr___02():

    interval = pitchtools.NamedHarmonicInterval('perfect', -1)
    repr = interval.__repr__()
    assert  repr == "NamedHarmonicInterval('P1')"

    interval = pitchtools.NamedHarmonicInterval('augmented', -1)
    repr = interval.__repr__()
    assert  repr == "NamedHarmonicInterval('aug1')"

    interval = pitchtools.NamedHarmonicInterval('minor', -2)
    repr = interval.__repr__()
    assert  repr == "NamedHarmonicInterval('m2')"

    interval = pitchtools.NamedHarmonicInterval('major', -2)
    repr = interval.__repr__()
    assert  repr == "NamedHarmonicInterval('M2')"

    interval = pitchtools.NamedHarmonicInterval('minor', -3)
    repr = interval.__repr__()
    assert  repr == "NamedHarmonicInterval('m3')"
