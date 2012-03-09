from abjad import *


def test_durtools_Duration__repr_with_tools_package_01():

    assert Duration(1, 4)._fully_qualified_repr == 'durationtools.Duration(1, 4)'
