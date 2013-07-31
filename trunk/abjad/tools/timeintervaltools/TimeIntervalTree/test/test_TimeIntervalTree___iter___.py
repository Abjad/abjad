# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools import *


def test_TimeIntervalTree___iter____01():
    blocks = timeintervaltools.make_test_intervals()
    tree = TimeIntervalTree(blocks)
    for e in enumerate(tree):
        assert blocks[e[0]] == e[1]
