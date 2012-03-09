from abjad import *


def test_instrumenttools_Flute__fully_qualified_repr_01():

    flute = instrumenttools.Flute()

    assert flute._fully_qualified_repr == 'instrumenttools.Flute()'
