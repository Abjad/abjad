# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import mathtools


def test_mathtools_weight_01():
    r'''Weight of nonempty sequence.
    '''

    assert mathtools.weight([-1, -2, 3, 4, 5]) == 15


def test_mathtools_weight_02():
    r'''Weight of empty sequence.
    '''

    assert mathtools.weight([]) == 0
