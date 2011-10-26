from abjad import *


def test_InstrumentationSpecifier__get_multiline_repr_01():

    flute = scoretools.Performer('Flute')
    flute.instruments.append(instrumenttools.Flute())
    flute.instruments.append(instrumenttools.AltoFlute())
    guitar = scoretools.Performer('Guitar')
    guitar.instruments.append(instrumenttools.Guitar())
    specifier = scoretools.InstrumentationSpecifier([flute, guitar])

    assert specifier._get_multiline_repr(include_tools_package=False) == [
        'InstrumentationSpecifier([',
        "    Performer('Flute', [Flute(), AltoFlute()]),",
        "    Performer('Guitar', [Guitar()])])"]


def test_InstrumentationSpecifier__get_multiline_repr_02():

    flute = scoretools.Performer('Flute')
    flute.instruments.append(instrumenttools.Flute())
    flute.instruments.append(instrumenttools.AltoFlute())
    guitar = scoretools.Performer('Guitar')
    guitar.instruments.append(instrumenttools.Guitar())
    specifier = scoretools.InstrumentationSpecifier([flute, guitar])

    assert specifier._get_multiline_repr(include_tools_package=True) == [
        'scoretools.InstrumentationSpecifier([',
        "    scoretools.Performer('Flute', ['instrumenttools.Flute()', 'instrumenttools.AltoFlute()']),",
        "    scoretools.Performer('Guitar', ['instrumenttools.Guitar()'])])"]
