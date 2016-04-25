# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_OrdinalConstant___format___01():
    r'''Ordinal constants are storable and the format is evaluable.
    '''

    vector_constant_1 = datastructuretools.OrdinalConstant('x', -1, 'Left')
    string = format(vector_constant_1)

    assert string == 'Left'
    vector_constant_2 = eval(string)

    assert isinstance(vector_constant_1, datastructuretools.OrdinalConstant)
    assert isinstance(vector_constant_2, datastructuretools.OrdinalConstant)
    assert not vector_constant_1 is vector_constant_2
    assert vector_constant_1 == vector_constant_2
