# -*- coding: utf-8 -*-
from abjad import *


def test_sievetools_Sieve___init___01():
    r'''Initialize sieve from rc instances and logical operator keyword.
    '''

    residue_classes = []
    residue_classes.append(sievetools.ResidueClass(6, 0))
    residue_classes.append(sievetools.ResidueClass(6, 1))
    residue_classes.append(sievetools.ResidueClass(6, 4))
    sieve = sievetools.Sieve(residue_classes, logical_operator='or')

    assert isinstance(sieve, sievetools.Sieve)
    assert sieve.residue_classes == residue_classes
    assert sieve.logical_operator == 'or'


def test_sievetools_Sieve___init___02():
    r'''Initialize sieve from other sieve instance.
    '''

    residue_classes = []
    residue_classes.append(sievetools.ResidueClass(6, 0))
    residue_classes.append(sievetools.ResidueClass(6, 1))
    residue_classes.append(sievetools.ResidueClass(6, 4))
    sieve = sievetools.Sieve(sievetools.Sieve(residue_classes, logical_operator='or'))

    assert isinstance(sieve, sievetools.Sieve)
    assert sieve.residue_classes == residue_classes
    assert sieve.logical_operator == 'or'