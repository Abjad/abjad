from abjad import *


def test_InstrumentationSpecifier__repr_with_tools_package_01():

    flute = scoretools.Performer('Flute')
    flute.instruments.append(instrumenttools.Flute())
    flute.instruments.append(instrumenttools.AltoFlute())
    guitar = scoretools.Performer('Guitar')
    guitar.instruments.append(instrumenttools.Guitar())
    specifier = scoretools.InstrumentationSpecifier([flute, guitar])
    
    assert specifier._repr_with_tools_package == "scoretools.InstrumentationSpecifier([scoretools.Performer(name='Flute', instruments=[instrumenttools.Flute(), instrumenttools.AltoFlute()]), scoretools.Performer(name='Guitar', instruments=[instrumenttools.Guitar()])])"
