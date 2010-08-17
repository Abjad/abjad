from abjad import *


def test_SchemeVectorConstant___init____01( ):

   vc = schemetools.SchemeVectorConstant(1, 2, 3, 4)
   assert str(vc) == '(1 2 3 4)'


def test_SchemeVectorConstant___init___02( ):

   vc = schemetools.SchemeVectorConstant(True, False, 1, 0)
   assert str(vc) == "(#t #f 1 0)"


def test_SchemeVectorConstant___init___03( ):

   vc = schemetools.SchemeVectorConstant(False, True, True)
   assert vc.format == "#'#(#f #t #t)"
