# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInterval___repr___01():

    interval = pitchtools.NamedInterval('perfect', 1)
    repr = interval.__repr__()
    assert  repr == "NamedInterval('P1')"

    interval = pitchtools.NamedInterval('augmented', 1)
    repr = interval.__repr__()
    assert  repr == "NamedInterval('+aug1')"

    interval = pitchtools.NamedInterval('minor', 2)
    repr = interval.__repr__()
    assert  repr == "NamedInterval('+m2')"

    interval = pitchtools.NamedInterval('major', 2)
    repr = interval.__repr__()
    assert  repr == "NamedInterval('+M2')"

    interval = pitchtools.NamedInterval('minor', 3)
    repr = interval.__repr__()
    assert  repr == "NamedInterval('+m3')"


def test_pitchtools_NamedInterval___repr___02():

    interval = pitchtools.NamedInterval('perfect', -1)
    repr = interval.__repr__()
    assert  repr == "NamedInterval('P1')"

    interval = pitchtools.NamedInterval('augmented', -1)
    repr = interval.__repr__()
    assert  repr == "NamedInterval('-aug1')"

    interval = pitchtools.NamedInterval('minor', -2)
    repr = interval.__repr__()
    assert  repr == "NamedInterval('-m2')"

    interval = pitchtools.NamedInterval('major', -2)
    repr = interval.__repr__()
    assert  repr == "NamedInterval('-M2')"

    interval = pitchtools.NamedInterval('minor', -3)
    repr = interval.__repr__()
    assert  repr == "NamedInterval('-m3')"
