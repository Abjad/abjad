# -*- coding: utf-8 -*-
from abjad import *


def test_sievetools_CompoundSieve___init___01():
    r'''Initialize sieve from rc instances and logical operator keyword.
    '''

    residue_classes = []
    residue_classes.append(sievetools.Sieve(6, 0))
    residue_classes.append(sievetools.Sieve(6, 1))
    residue_classes.append(sievetools.Sieve(6, 4))
    sieve = sievetools.CompoundSieve(residue_classes, logical_operator='or')

    assert isinstance(sieve, sievetools.CompoundSieve)
    assert sieve.residue_classes == residue_classes
    assert sieve.logical_operator == 'or'