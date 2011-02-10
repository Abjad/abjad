from abjad import *


def test_SchemeNumber___eq___01( ):

   a = schemetools.SchemeNumber(3)
   b = schemetools.SchemeNumber(4)

   assert a != b

def test_SchemeNumber___eq___02( ):

   a = schemetools.SchemeNumber(3)
   b = schemetools.SchemeNumber(3)

   assert a == b

def test_SchemeNumber___eq___03( ):

   a = schemetools.SchemeNumber(3)
   b = schemetools.SchemeNumber(3.0)

   assert a == b
