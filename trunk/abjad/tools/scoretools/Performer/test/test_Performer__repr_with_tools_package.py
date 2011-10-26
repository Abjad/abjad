from abjad import *


def test_Performer__repr_with_tools_package_01():

    performer = scoretools.Performer('Flute')
    performer.instruments.append(instrumenttools.Flute())
    performer.instruments.append(instrumenttools.AltoFlute())

    assert performer._repr_with_tools_package == \
        "scoretools.Performer('Flute', ['instrumenttools.Flute()', 'instrumenttools.AltoFlute()'])"
