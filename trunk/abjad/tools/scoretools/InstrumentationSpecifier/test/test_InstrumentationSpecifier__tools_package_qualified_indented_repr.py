from abjad import *
import py


def test_InstrumentationSpecifier__tools_package_qualified_indented_repr_01():
    py.test.skip('make the indentend repr work.')

    flute = scoretools.Performer('Flute')
    flute.instruments.append(instrumenttools.Flute())
    flute.instruments.append(instrumenttools.AltoFlute())
    guitar = scoretools.Performer('Guitar')
    guitar.instruments.append(instrumenttools.Guitar())
    specifier = scoretools.InstrumentationSpecifier([flute, guitar])
    
    assert specifier._tools_package_qualified_repr == "scoretools.InstrumentationSpecifier([scoretools.Performer(name='Flute', instruments=[instrumenttools.Flute(), instrumenttools.AltoFlute()]), scoretools.Performer(name='Guitar', instruments=[instrumenttools.Guitar()])])"

    assert specifier._tools_package_qualifier_indented_repr == '???'
