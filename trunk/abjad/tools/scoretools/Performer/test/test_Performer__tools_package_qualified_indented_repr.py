from abjad import *
import py


def test_Performer__tools_package_qualified_indented_repr_01():
    py.test.skip('make indented repr work.')

    performer = scoretools.Performer('Flute')
    performer.instruments.append(instrumenttools.Flute())
    performer.instruments.append(instrumenttools.AltoFlute())

    assert performer._tools_package_qualified_repr == "scoretools.Performer(name='Flute', instruments=[instrumenttools.Flute(), instrumenttools.AltoFlute()])"

    assert performer._tools_package_qualified_indented_repr == '???'
