# -*- encoding: utf-8 -*-
from abjad import *


def test_mathtools_NonreducedRatio___init___01():
    r'''Initializes nonreduced ratio from empty input.
    '''

    ratio = mathtools.NonreducedRatio()

    assert ratio == mathtools.NonreducedRatio(1, 1)
