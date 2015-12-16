# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import sievetools


def test_sievetools_Sieve_representative_boolean_train_01():

    sieve = sievetools.ResidueClass(5, 0)
    sieve = sieve | sievetools.ResidueClass(5, 1)
    sieve = sieve | sievetools.ResidueClass(6, 0)
    sieve = sieve | sievetools.ResidueClass(6, 1)

    boolean_train = sieve.representative_boolean_train
    assert boolean_train == [
        1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1,
        1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0,
        ]
    assert len(boolean_train) == sieve.period


def test_sievetools_Sieve_representative_boolean_train_02():

    sieve = sievetools.ResidueClass(3, 0) | sievetools.ResidueClass(3, 1)

    boolean_train = sieve.representative_boolean_train
    assert boolean_train == [1, 1, 0]
    assert len(boolean_train) == sieve.period