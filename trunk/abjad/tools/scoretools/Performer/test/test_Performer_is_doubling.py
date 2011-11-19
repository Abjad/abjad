from abjad import *


def test_Performer_is_doubling_01():

    performer = scoretools.Performer('Flutist')
    performer.instruments.append(instrumenttools.Flute())
    assert not performer.is_doubling

    performer.instruments.append(instrumenttools.Piccolo())
    assert performer.is_doubling
