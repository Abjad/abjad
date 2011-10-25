from abjad import *


def test_Performer_instruments_01():

    performer = scoretools.Performer('Flutist')
    assert performer.instruments == []

    performer.instruments.append(scoretools.Flute())
    flute = scoretools.Flute()
    assert flute in performer.instruments

    performer.instruments.append(scoretools.Piccolo())
    piccolo = scoretools.Piccolo()
    assert piccolo in performer.instruments

    assert len(performer.instruments) == 2

    performer.instruments = None
    assert len(performer.instruments) == 0
