from abjad import *


def test_SchemeVector___init___01( ):

   vector = schemetools.SchemeVector(1, 2, 3, 4)
   assert str(vector) == '(1 2 3 4)'
