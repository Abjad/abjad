from abjad import *
from abjad.tools import instrumenttools


def test_HumanMusician_instruments_01():

    human_musician = instrumenttools.HumanMusician('Flutist')
    assert human_musician.instruments == []

    human_musician.instruments.append(instrumenttools.Flute())
    flute = instrumenttools.Flute()
    assert flute in human_musician.instruments

    human_musician.instruments.append(instrumenttools.Piccolo())
    piccolo = instrumenttools.Piccolo()
    assert piccolo in human_musician.instruments

    assert len(human_musician.instruments) == 2

    human_musician.instruments = None
    assert len(human_musician.instruments) == 0
