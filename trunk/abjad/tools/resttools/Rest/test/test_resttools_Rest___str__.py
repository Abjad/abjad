# -*- encoding: utf-8 -*-
from abjad import *


def test_resttools_Rest___str___01():

    rest = Rest((1, 4))

    assert str(rest) == 'r4'
