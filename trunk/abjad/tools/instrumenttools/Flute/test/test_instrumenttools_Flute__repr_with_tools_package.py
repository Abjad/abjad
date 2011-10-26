from abjad import *


def test_instrumenttools_Flute__repr_with_tools_package_01():

    flute = instrumenttools.Flute()

    assert flute._repr_with_tools_package == 'instrumenttools.Flute()'
