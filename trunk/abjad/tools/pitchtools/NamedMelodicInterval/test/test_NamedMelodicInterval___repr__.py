# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicInterval___repr___01():

    interval = pitchtools.NamedMelodicInterval('perfect', 1)
    repr = interval.__repr__()
    assert  repr == "NamedMelodicInterval('P1')"

    interval = pitchtools.NamedMelodicInterval('augmented', 1)
    repr = interval.__repr__()
    assert  repr == "NamedMelodicInterval('+aug1')"

    interval = pitchtools.NamedMelodicInterval('minor', 2)
    repr = interval.__repr__()
    assert  repr == "NamedMelodicInterval('+m2')"

    interval = pitchtools.NamedMelodicInterval('major', 2)
    repr = interval.__repr__()
    assert  repr == "NamedMelodicInterval('+M2')"

    interval = pitchtools.NamedMelodicInterval('minor', 3)
    repr = interval.__repr__()
    assert  repr == "NamedMelodicInterval('+m3')"


def test_NamedMelodicInterval___repr___02():

    interval = pitchtools.NamedMelodicInterval('perfect', -1)
    repr = interval.__repr__()
    assert  repr == "NamedMelodicInterval('P1')"

    interval = pitchtools.NamedMelodicInterval('augmented', -1)
    repr = interval.__repr__()
    assert  repr == "NamedMelodicInterval('-aug1')"

    interval = pitchtools.NamedMelodicInterval('minor', -2)
    repr = interval.__repr__()
    assert  repr == "NamedMelodicInterval('-m2')"

    interval = pitchtools.NamedMelodicInterval('major', -2)
    repr = interval.__repr__()
    assert  repr == "NamedMelodicInterval('-M2')"

    interval = pitchtools.NamedMelodicInterval('minor', -3)
    repr = interval.__repr__()
    assert  repr == "NamedMelodicInterval('-m3')"
