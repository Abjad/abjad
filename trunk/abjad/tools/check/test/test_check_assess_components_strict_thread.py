from abjad import *
import py.test


def test_assess_components_strict_thread_01( ):
   '''True for strictly contiguous leaves in same staff.'''

   t = Staff(scale(4))
   assert check.assess_components(t[:], contiguity = 'strict', share = 'thread')


def test_assess_components_strict_thread_02( ):
   '''True for orphan components when allow_orphans is True.
      False for orphan components when allow_orphans is False.'''

   assert check.assess_components(scale(4), contiguity = 'strict', share = 'thread')
   assert not check.assess_components(scale(4), allow_orphans = False, 
      contiguity = 'strict', share = 'thread')


def test_assess_components_strict_thread_03( ):
   '''False for time reordered leaves in staff.'''

   t = Staff(scale(4))
   assert not check.assess_components(t[2:] + t[:2], 
      contiguity = 'strict', share = 'thread')


def test_assess_components_strict_thread_04( ):
   '''False for unincorporated component.'''

   assert check.assess_components([Staff(scale(4))], 
      contiguity = 'strict', share = 'thread')


def test_assess_components_strict_thread_05( ):
   '''True for empty list.'''

   assert check.assess_components([ ], contiguity = 'strict', share = 'thread')
