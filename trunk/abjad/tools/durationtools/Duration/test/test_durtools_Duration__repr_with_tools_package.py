from abjad import *


def test_durtools_Duration__fully_qualified_repr_01():

    assert Duration(1, 4)._fully_qualified_repr == 'durationtools.Duration(1, 4)'
