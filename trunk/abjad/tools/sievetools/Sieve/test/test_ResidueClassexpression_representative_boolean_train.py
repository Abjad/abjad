from abjad import *
from abjad.tools import sievetools


RC = sievetools.ResidueClass

def test_ResidueClassexpression_representative_boolean_train_01():

    sieve = RC(5, 0) | RC(5, 1) | RC(6, 0) | RC(6, 1)

    t = sieve.representative_boolean_train
    assert t == [1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1,
        1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0]
    assert len(t) == sieve.period


def test_ResidueClassexpression_representative_boolean_train_02():

    sieve = RC(3, 0) | RC(3, 1)

    t = sieve.representative_boolean_train
    assert t == [1, 1, 0]
    assert len(t) == sieve.period
