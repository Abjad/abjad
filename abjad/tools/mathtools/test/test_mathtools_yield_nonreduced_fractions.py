# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import durationtools


def test_mathtools_yield_nonreduced_fractions_01():

    generator = mathtools.yield_nonreduced_fractions()

    assert next(generator) == (1, 1)
    assert next(generator) == (2, 1)
    assert next(generator) == (1, 2)
    assert next(generator) == (1, 3)
    assert next(generator) == (2, 2)
    assert next(generator) == (3, 1)
    assert next(generator) == (4, 1)
    assert next(generator) == (3, 2)
    assert next(generator) == (2, 3)
    assert next(generator) == (1, 4)
    assert next(generator) == (1, 5)
    assert next(generator) == (2, 4)
