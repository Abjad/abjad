# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_yield_all_k_ary_sequences_of_length_01():

    generator = sequencetools.yield_all_k_ary_sequences_of_length(2, 3)

    assert next(generator) == (0, 0, 0)
    assert next(generator) == (0, 0, 1)
    assert next(generator) == (0, 1, 0)
    assert next(generator) == (0, 1, 1)
    assert next(generator) == (1, 0, 0)
    assert next(generator) == (1, 0, 1)
    assert next(generator) == (1, 1, 0)
    assert next(generator) == (1, 1, 1)
