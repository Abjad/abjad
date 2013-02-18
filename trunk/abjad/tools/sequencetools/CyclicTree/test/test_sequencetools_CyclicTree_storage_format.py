from abjad import *


def test_sequencetools_CyclicTree_storage_format_01():

    cyclic_tree = sequencetools.CyclicTree([[1, 2, 3], [4, 5]])

    r'''
    sequencetools.CyclicTree(
        [1, 2, 3],
        [4, 5]
        )
    '''

    assert cyclic_tree.storage_format == 'sequencetools.CyclicTree(\n\t[1, 2, 3],\n\t[4, 5]\n\t)'
