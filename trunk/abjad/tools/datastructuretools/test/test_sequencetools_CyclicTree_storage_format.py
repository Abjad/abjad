# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_CyclicTree_storage_format_01():

    cyclic_tree = datastructuretools.CyclicPayloadTree([[1, 2, 3], [4, 5]])

    r'''
    datastructuretools.CyclicPayloadTree(
        [1, 2, 3],
        [4, 5]
        )
    '''

    assert cyclic_tree.storage_format == 'datastructuretools.CyclicPayloadTree(\n\t[[1, 2, 3], [4, 5]]\n\t)'
