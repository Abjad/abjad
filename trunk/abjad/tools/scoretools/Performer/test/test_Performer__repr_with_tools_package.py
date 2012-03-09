from abjad import *


def test_Performer__fully_qualified_repr_01():

    performer = scoretools.Performer('Flute')
    performer.instruments.append(instrumenttools.Flute())
    performer.instruments.append(instrumenttools.AltoFlute())

    assert performer._fully_qualified_repr == \
        "scoretools.Performer(name='Flute', instruments=[instrumenttools.Flute(), instrumenttools.AltoFlute()])"
