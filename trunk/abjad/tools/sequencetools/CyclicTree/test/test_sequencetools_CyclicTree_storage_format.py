from abjad.tools import sequencetools


def test_sequencetools_CyclicTree_storage_format_01():

    cyclic_tree = sequencetools.CyclicTree([[1, 2, 3], [4, 5]])

    assert cyclic_tree.storage_format == 'sequencetools.CyclicTree(\n\t[[1, 2, 3], [4, 5]]\n\t)'
