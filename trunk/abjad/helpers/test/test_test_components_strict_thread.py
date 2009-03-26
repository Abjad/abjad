from abjad import *
import py.test


def test_assess_components_strict_thread_01( ):
   '''True for strictly contiguous leaves in same staff.'''

   t = Staff(scale(4))
   assert assess_components(t[:], contiguity = 'strict', share = 'thread')


def test_assess_components_strict_thread_02( ):
   '''True for orphan components when allow_orphans is True.
      False for orphan components when allow_orphans is False.'''

   assert assess_components(scale(4), contiguity = 'strict', share = 'thread')
   assert not assess_components(scale(4), allow_orphans = False, 
      contiguity = 'strict', share = 'thread')


def test_assess_components_strict_thread_03( ):
   '''False for time reordered leaves in staff.'''

   t = Staff(scale(4))
   assert not assess_components(t[2:] + t[:2], 
      contiguity = 'strict', share = 'thread')


def test_assess_components_strict_thread_04( ):
   '''False for unincorporated component.'''

   py.test.skip('TODO: Active proposal that staves and staff groups should not thread. Outcome of that proposal will determine the behavior of this test.')
   assert not assess_components([Staff(scale(4))], 
      contiguity = 'strict', share = 'thread')


def test_assess_components_strict_thread_05( ):
   '''True for empty list.'''

   assert assess_components([ ], contiguity = 'strict', share = 'thread')
