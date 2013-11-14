# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sievetools


def test_sievetools_ResidueClass___init___01():
    r'''Initialize from modulo and residue.
    '''

    rc = sievetools.ResidueClass(6, 0)

    assert isinstance(rc, sievetools.ResidueClass)
    assert rc.modulo == 6
    assert rc.residue == 0


def test_sievetools_ResidueClass___init___02():
    r'''Initialize from other rc instance.
    '''

    rc = sievetools.ResidueClass(sievetools.ResidueClass(6, 0))

    assert isinstance(rc, sievetools.ResidueClass)
    assert rc.modulo == 6
    assert rc.residue == 0
