# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Tuplet___init___01():
    r'''Initializes tuplet from empty input.
    '''

    tuplet = Tuplet()

    assert format(tuplet) == '\\times 2/3 {\n}'
    assert tuplet.multiplier == Multiplier(2, 3)
    assert not len(tuplet)
