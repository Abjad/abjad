from abjad import *


def test_SchemeVector___init____01( ):

   vector = schemetools.SchemeVector(1, 2, 3, 4)
   assert str(vector) == '(1 2 3 4)'


def test_SchemeVector___init____02( ):

   vector = schemetools.SchemeVector(True, False, 1, 0)
   assert str(vector) == "(#t #f 1 0)"


def test_SchemeVector___init____03( ):

   vector = schemetools.SchemeVector(0, 1, 2)
   assert vector.format == "#'(0 1 2)"
