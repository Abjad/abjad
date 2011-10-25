from abjad import *
from abjad.tools import instrumenttools


def test_Performer_instruments_01():

    performer = scoretools.Performer('Flutist')
    assert performer.instruments == []

    performer.instruments.append(instrumenttools.Flute())
    flute = instrumenttools.Flute()
    assert flute in performer.instruments

    performer.instruments.append(instrumenttools.Piccolo())
    piccolo = instrumenttools.Piccolo()
    assert piccolo in performer.instruments

    assert len(performer.instruments) == 2

    performer.instruments = None
    assert len(performer.instruments) == 0
