from abjad import *


def test_override_getitem_01( ):
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   override = Override(staff[ : 4], 'Beam', 'positions', (8, 8))
   for i in range(4):
      assert override.components[i] == staff[i]


def test_override_getitem_02( ):
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   override = Override(staff[ : 4], 'Beam', 'positions', (8, 8))
   assert override.components[1 : 3] == tuple(staff[1 : 3])


def test_override_getitem_03( ):
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   override = Override(staff[ : 4], 'Beam', 'positions', (8, 8))
   assert override.components[1 : ] == tuple(staff[1 : 4])


def test_override_getitem_04( ):
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   override = Override(staff[ : 4], 'Beam', 'positions', (8, 8))
   assert override.components[ : -1] == tuple(staff[ : 3])
