# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sievetools


RC = sievetools.ResidueClass

def test_sievetools_Sieve_period_01():

    sieve = RC(5, 0) | RC(5, 1) | RC(6, 0) | RC(6, 1)

    "{RC(5, 0) | RC(5, 1) | RC(6, 0) | RC(6, 1)}"

    assert sieve.period == 30


def test_sievetools_Sieve_period_02():

    sieve = RC(3, 0) | RC(3, 1)

    "{RC(3, 0) | RC(3, 1)}"

    assert sieve.period == 3