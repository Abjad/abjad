# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import sievetools


def test_sievetools_CompoundSieve__sort_residue_classes_01():
    r'''Unsorted RCs are sorted on sieve initialization.
    '''

    RC = sievetools.ResidueClass
    sieve = sievetools.CompoundSieve([RC(10, 0), RC(9, 0), RC(8, 0)])
    assert sieve.residue_classes == [RC(8, 0), RC(9, 0), RC(10, 0)]


def test_sievetools_CompoundSieve__sort_residue_classes_02():
    r'''Unsorted RCs are sorted on sieve initialization.
    '''

    RC = sievetools.ResidueClass
    sieve = sievetools.CompoundSieve([RC(8, 7), RC(8, 1), RC(8, 2)])
    assert sieve.residue_classes == [RC(8, 1), RC(8, 2), RC(8, 7)]