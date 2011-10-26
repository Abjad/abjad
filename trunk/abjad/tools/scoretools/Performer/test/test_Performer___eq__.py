from abjad import *


def test_Performer___eq___01():

    performer_1 = scoretools.Performer('Flute')
    performer_1.instruments.append(instrumenttools.Flute())
    performer_1.instruments.append(instrumenttools.AltoFlute())

    performer_2 = scoretools.Performer('Flute')
    performer_2.instruments.append(instrumenttools.AltoFlute())
    performer_2.instruments.append(instrumenttools.Flute())

    assert performer_1 == performer_2
    assert performer_2 == performer_1

    assert not performer_1 != performer_2
    assert not performer_2 != performer_1
