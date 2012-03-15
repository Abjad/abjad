from abjad import *


def test_durationtools_Duration__tools_package_qualified_repr_01():

    assert Duration(1, 4)._tools_package_qualified_repr == 'durationtools.Duration(1, 4)'
