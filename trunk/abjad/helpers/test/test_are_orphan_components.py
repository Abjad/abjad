from abjad.helpers.are_orphan_components import _are_orphan_components
from abjad import *


def test_are_orphan_components_01( ):
   '''True when each of the elements is an orphan.'''

   t = scale(4)
   assert _are_orphan_components(t)


def test_are_orphan_components_02( ):
   '''False when any of the elements have a parent.'''

   t = Staff(scale(4))
   assert not _are_orphan_components(t)


def test_are_orphan_components_03( ):
   '''True for list of length 0.'''

   assert _are_orphan_components([ ])


def test_are_orphan_components_04( ):
   '''False for single Abjad components.'''

   assert not _are_orphan_components(Note(0, (1, 4))) 


def test_are_orhan_components_05( ):
   '''False when any of the elements are not Abjad components.'''

   assert not _are_orphan_components([1, 2, 3])
