from abjad import *
from abjad.tools import sievetools


def test_ResidueClassexpression___init___01():
    '''Init sieve from rc instances and operator keyword.'''

    rcs = []
    rcs.append(sievetools.ResidueClass(6, 0))
    rcs.append(sievetools.ResidueClass(6, 1))
    rcs.append(sievetools.ResidueClass(6, 4))
    sieve = sievetools.ResidueClassExpression(rcs, operator = 'or')

    assert isinstance(sieve, sievetools.ResidueClassExpression)
    assert sieve.rcs == rcs
    assert sieve.operator == 'or'


def test_ResidueClassexpression___init___02():
    '''Init sieve from other sieve instance.'''

    rcs = []
    rcs.append(sievetools.ResidueClass(6, 0))
    rcs.append(sievetools.ResidueClass(6, 1))
    rcs.append(sievetools.ResidueClass(6, 4))
    sieve = sievetools.ResidueClassExpression(sievetools.ResidueClassExpression(rcs, operator = 'or'))

    assert isinstance(sieve, sievetools.ResidueClassExpression)
    assert sieve.rcs == rcs
    assert sieve.operator == 'or'
