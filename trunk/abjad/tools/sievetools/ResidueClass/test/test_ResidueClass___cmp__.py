from abjad import *
from abjad.tools import sievetools


def test_ResidueClass___cmp___01():

    rc1 = sievetools.ResidueClass(6, 0)
    rc2 = sievetools.ResidueClass(6, 1)

    assert not rc1 == rc2
    assert rc1 != rc2
    assert rc1 < rc2
    assert rc1 <= rc2
    assert not rc1 > rc2
    assert not rc1 >= rc2


def test_ResidueClass___cmp___02():

    rc1 = sievetools.ResidueClass(6, 0)
    rc2 = sievetools.ResidueClass(7, 0)

    assert not rc1 == rc2
    assert rc1 != rc2
    assert rc1 < rc2
    assert rc1 <= rc2
    assert not rc1 > rc2
    assert not rc1 >= rc2


def test_ResidueClass___cmp___03():

    rc1 = sievetools.ResidueClass(6, 0)
    rc2 = sievetools.ResidueClass(6, 0)

    assert rc1 == rc2
    assert not rc1 != rc2
    assert not rc1 < rc2
    assert rc1 <= rc2
    assert not rc1 > rc2
    assert rc1 >= rc2
