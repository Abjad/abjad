# -*- coding: utf-8 -*-
from abjad import *


def test_schemetools_SchemeVectorConstant___init___01():

    vc = schemetools.SchemeVectorConstant(1, 2, 3, 4)
    assert str(vc) == "'#(1 2 3 4)"
    assert format(vc) == "#'#(1 2 3 4)"



def test_schemetools_SchemeVectorConstant___init___02():

    vc = schemetools.SchemeVectorConstant(True, False, 1, 0)
    assert str(vc) == "'#(#t #f 1 0)"
    assert format(vc) == "#'#(#t #f 1 0)"
