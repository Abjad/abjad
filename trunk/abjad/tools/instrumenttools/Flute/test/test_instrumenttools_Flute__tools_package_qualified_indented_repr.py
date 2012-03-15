from abjad import *


def test_instrumenttools_Flute__tools_package_qualified_indented_repr_01():

    flute = instrumenttools.Flute()

    assert flute._tools_package_qualified_repr == 'instrumenttools.Flute()'
    assert flute._tools_package_qualified_indented_repr == 'instrumenttools.Flute()'
