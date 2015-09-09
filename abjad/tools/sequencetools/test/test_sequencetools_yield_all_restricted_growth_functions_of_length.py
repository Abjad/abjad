# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_yield_all_restricted_growth_functions_of_length_01():

    rgfs = sequencetools.yield_all_restricted_growth_functions_of_length(3)

    assert next(rgfs) == (1, 1, 1)
    assert next(rgfs) == (1, 1, 2)
    assert next(rgfs) == (1, 2, 1)
    assert next(rgfs) == (1, 2, 2)
    assert next(rgfs) == (1, 2, 3)


def test_sequencetools_yield_all_restricted_growth_functions_of_length_02():

    rgfs = sequencetools.yield_all_restricted_growth_functions_of_length(4)

    assert next(rgfs) == (1, 1, 1, 1)
    assert next(rgfs) == (1, 1, 1, 2)
    assert next(rgfs) == (1, 1, 2, 1)
    assert next(rgfs) == (1, 1, 2, 2)
    assert next(rgfs) == (1, 1, 2, 3)
    assert next(rgfs) == (1, 2, 1, 1)
    assert next(rgfs) == (1, 2, 1, 2)
    assert next(rgfs) == (1, 2, 1, 3)
    assert next(rgfs) == (1, 2, 2, 1)
    assert next(rgfs) == (1, 2, 2, 2)
    assert next(rgfs) == (1, 2, 2, 3)
    assert next(rgfs) == (1, 2, 3, 1)
    assert next(rgfs) == (1, 2, 3, 2)
    assert next(rgfs) == (1, 2, 3, 3)
    assert next(rgfs) == (1, 2, 3, 4)
