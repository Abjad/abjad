from abjad import *
from abjad.tools import sievetools


RC = sievetools.ResidueClass

def test_ResidueClassexpression_representative_congruent_bases_01():

    sieve = RC(5, 0) | RC(5, 1) | RC(6, 0) | RC(6, 1)

    assert sieve.representative_congruent_bases == [
        0, 1, 5, 6, 7, 10, 11, 12, 13, 15, 16, 18, 19, 20, 21, 24, 25, 26]


def test_ResidueClassexpression_representative_congruent_bases_02():

    sieve = RC(3, 0) | RC(3, 1)

    assert sieve.representative_congruent_bases == [0, 1]
