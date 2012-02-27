from abjad import *


def test_durtools_Duration__repr_with_tools_package_01():

    assert Duration(1, 4)._repr_with_tools_package == 'durationtools.Duration(1, 4)'
