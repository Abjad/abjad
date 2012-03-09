from abjad import *


def test_InstrumentationSpecifier__fully_qualified_repr_01():

    flute = scoretools.Performer('Flute')
    flute.instruments.append(instrumenttools.Flute())
    flute.instruments.append(instrumenttools.AltoFlute())
    guitar = scoretools.Performer('Guitar')
    guitar.instruments.append(instrumenttools.Guitar())
    specifier = scoretools.InstrumentationSpecifier([flute, guitar])
    
    assert specifier._fully_qualified_repr == "scoretools.InstrumentationSpecifier([scoretools.Performer(name='Flute', instruments=[instrumenttools.Flute(), instrumenttools.AltoFlute()]), scoretools.Performer(name='Guitar', instruments=[instrumenttools.Guitar()])])"
