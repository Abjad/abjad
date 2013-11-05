# -*- encoding: utf-8 -*-
from abjad import *


def test_sievetools_Sieve___init___01():
    r'''Init sieve from rc instances and logical operator keyword.
    '''

    rcs = []
    rcs.append(sievetools.ResidueClass(6, 0))
    rcs.append(sievetools.ResidueClass(6, 1))
    rcs.append(sievetools.ResidueClass(6, 4))
    sieve = sievetools.Sieve(rcs, logical_operator='or')

    assert isinstance(sieve, sievetools.Sieve)
    assert sieve.rcs == rcs
    assert sieve.logical_operator == 'or'


def test_sievetools_Sieve___init___02():
    r'''Init sieve from other sieve instance.
    '''

    rcs = []
    rcs.append(sievetools.ResidueClass(6, 0))
    rcs.append(sievetools.ResidueClass(6, 1))
    rcs.append(sievetools.ResidueClass(6, 4))
    sieve = sievetools.Sieve(sievetools.Sieve(rcs, logical_operator='or'))

    assert isinstance(sieve, sievetools.Sieve)
    assert sieve.rcs == rcs
    assert sieve.logical_operator == 'or'
