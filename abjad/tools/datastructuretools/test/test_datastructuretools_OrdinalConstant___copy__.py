# -*- coding: utf-8 -*-
import copy
from abjad import *


def test_datastructuretools_OrdinalConstant___copy___01():

    constant_1 = datastructuretools.OrdinalConstant('x', -1, 'left')
    constant_2 = copy.deepcopy(constant_1)

    assert isinstance(constant_1, datastructuretools.OrdinalConstant)
    assert isinstance(constant_2, datastructuretools.OrdinalConstant)
    assert not constant_1 is constant_2
    assert constant_1 == constant_2
