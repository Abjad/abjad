from abjad import *


def test_OverrideSpanner___getitem___01( ):
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   override = OverrideSpanner(staff[ : 4], 'Beam', 'positions', (8, 8))
   for i in range(4):
      assert override.components[i] == staff[i]


def test_OverrideSpanner___getitem___02( ):
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   override = OverrideSpanner(staff[ : 4], 'Beam', 'positions', (8, 8))
   assert override.components[1 : 3] == tuple(staff[1 : 3])


def test_OverrideSpanner___getitem___03( ):
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   override = OverrideSpanner(staff[ : 4], 'Beam', 'positions', (8, 8))
   assert override.components[1 : ] == tuple(staff[1 : 4])


def test_OverrideSpanner___getitem___04( ):
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   override = OverrideSpanner(staff[ : 4], 'Beam', 'positions', (8, 8))
   assert override.components[ : -1] == tuple(staff[ : 3])
