from abjad.helpers.are_strictly_contiguous_components_in_same_thread import _are_strictly_contiguous_components_in_same_thread
from abjad import *
import py.test


def test_are_strictly_contiguous_components_in_same_thread_01( ):
   '''True for strictly contiguous leaves in same staff.'''

   t = Staff(scale(4))
   assert _are_strictly_contiguous_components_in_same_thread(t[:])


def test_are_strictly_contiguous_components_in_same_thread_02( ):
   '''False for unincorporated components.'''

   assert not _are_strictly_contiguous_components_in_same_thread(scale(4))


def test_are_strictly_contiguous_components_in_same_thread_03( ):
   '''False for time reordered leaves in staff.'''

   t = Staff(scale(4))
   assert not _are_strictly_contiguous_components_in_same_thread(t[2:] + t[:2])


def test_are_strictly_contiguous_components_in_same_thread_04( ):
   '''False for unincorporated component.'''

   py.test.skip('TODO: Active proposal that staves and staff groups should not thread. Outcome of that proposal will determine the behavior of this test.')
   assert not _are_strictly_contiguous_components_in_same_thread(
      [Staff(scale(4))])


def test_are_strictly_contiguous_components_in_same_thread_05( ):
   '''True for empty list.'''

   assert _are_strictly_contiguous_components_in_same_thread([ ])
