from abjad import *


def test_assess_components_none_none_01( ):
   t = scale(4)
   assert assess_components(t)


def test_assess_components_none_none_02( ):
   t = Staff(scale(4)) * 4
   assert assess_components(t)


def test_assess_components_none_none_03( ):
   t = range(4)
   assert not assess_components(t)


def test_assess_components_none_none_04( ):
   t = [ ]
   assert assess_components(t)
