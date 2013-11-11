# -*- encoding: utf-8 -*-
from abjad import *


def test_datastructuretools_CyclicTree___format___01():

    cyclic_tree = datastructuretools.CyclicPayloadTree([[1, 2, 3], [4, 5]])

    # TODO: make fully recursive to indent at multiple levels
    assert systemtools.TestManager.compare(
        format(cyclic_tree),
        r'''
        datastructuretools.CyclicPayloadTree(
            [[1, 2, 3], [4, 5]]
            )
        '''
        )
