from abjad import *


def test_SchemeNumber___float___01( ):

   a = schemetools.SchemeNumber(-1)

   assert float(a) == -1.0
