from abjad import *


def test_durationtools_Duration__tools_package_qualified_indented_repr_01():

    assert Duration(1, 4)._tools_package_qualified_indented_repr == 'durationtools.Duration(\n\t1,\n\t4\n\t)'

    r'''
    durationtools.Duration(
        1,
        4
        )
    '''
