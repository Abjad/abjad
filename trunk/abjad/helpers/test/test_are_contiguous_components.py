from abjad.helpers.are_contiguous_components import _are_contiguous_components
from abjad import *


def test_are_contiguous_components_01( ):
   '''Return True when are all contiguous components.'''

   t = Staff(scale(4))
   assert _are_contiguous_components(t[:])


def test_are_contiguous_components_02( ):
   '''False on orphan components.'''

   assert not _are_contiguous_components(scale(4))


def test_are_contiguous_components_03( ):
   '''False on scrambled sibling components.'''

   t = Staff(scale(4))
   assert not _are_contiguous_components(t[2:] + t[:2])


def test_are_contiguous_components_04( ):
   '''False on lone component.'''

   assert not _are_contiguous_components(Staff(scale(4)))


def test_are_contiguous_components_05( ):
   '''True on empty list.'''

   assert _are_contiguous_components([ ])
