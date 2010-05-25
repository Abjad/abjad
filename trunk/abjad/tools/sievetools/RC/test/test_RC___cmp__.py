from abjad import *


def test_RC___cmp___01( ):

   rc1 = sievetools.RC(6, 0)
   rc2 = sievetools.RC(6, 1)

   assert not rc1 == rc2
   assert rc1 != rc2
   assert rc1 < rc2
   assert rc1 <= rc2
   assert not rc1 > rc2
   assert not rc1 >= rc2


def test_RC___cmp___02( ):

   rc1 = sievetools.RC(6, 0)
   rc2 = sievetools.RC(7, 0)

   assert not rc1 == rc2
   assert rc1 != rc2
   assert rc1 < rc2
   assert rc1 <= rc2
   assert not rc1 > rc2
   assert not rc1 >= rc2


def test_RC___cmp___03( ):

   rc1 = sievetools.RC(6, 0)
   rc2 = sievetools.RC(6, 0)

   assert rc1 == rc2
   assert not rc1 != rc2
   assert not rc1 < rc2
   assert rc1 <= rc2
   assert not rc1 > rc2
   assert rc1 >= rc2
