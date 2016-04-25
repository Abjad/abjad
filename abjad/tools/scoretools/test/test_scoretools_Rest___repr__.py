# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Rest___repr___01():
    r'''Rest repr is evaluable.
    '''

    rest_1 = Rest((1, 4))
    rest_2 = eval(repr(rest_1))

    assert isinstance(rest_1, Rest)
    assert isinstance(rest_2, Rest)
    assert format(rest_1) == format(rest_2)
    assert rest_1 is not rest_2
