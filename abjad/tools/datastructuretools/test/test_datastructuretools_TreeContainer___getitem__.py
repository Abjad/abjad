# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_datastructuretools_TreeContainer___getitem___01():

    leaf_a = datastructuretools.TreeNode()
    leaf_b = datastructuretools.TreeNode()
    leaf_c = datastructuretools.TreeNode()

    container = datastructuretools.TreeContainer([leaf_a, leaf_b, leaf_c])

    assert container[0] is leaf_a
    assert container[1] is leaf_b
    assert container[2] is leaf_c

    pytest.raises(Exception, 'container[3]')

    assert container[-1] is leaf_c
    assert container[-2] is leaf_b
    assert container[-3] is leaf_a

    pytest.raises(Exception, 'container[-4]')
