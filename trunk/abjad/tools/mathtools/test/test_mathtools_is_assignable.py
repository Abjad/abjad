from abjad import *


def test_mathtools_is_assignable_01( ):
   '''True when integer n can be written without
   recourse to ties. Otherwise false.
   '''

   assert not mathtools.is_assignable(0)
   assert mathtools.is_assignable(1)
   assert mathtools.is_assignable(2)
   assert mathtools.is_assignable(3)
   assert mathtools.is_assignable(4)
   assert not mathtools.is_assignable(5)
   assert mathtools.is_assignable(6)
   assert mathtools.is_assignable(7)
   assert mathtools.is_assignable(8)


def test_mathtools_is_assignable_02( ):

   assert not mathtools.is_assignable(9)
   assert not mathtools.is_assignable(10)
   assert not mathtools.is_assignable(11)
   assert mathtools.is_assignable(12)
   assert not mathtools.is_assignable(13)
   assert mathtools.is_assignable(14)
   assert mathtools.is_assignable(15)
   assert mathtools.is_assignable(16)
