from abjad import *
import py.test


def test_componenttools_all_are_contiguous_components_in_same_thread_01( ):
   '''True for strictly contiguous leaves in same staff.'''

   t = Staff(macros.scale(4))
   assert componenttools.all_are_contiguous_components_in_same_thread(t[:])


def test_componenttools_all_are_contiguous_components_in_same_thread_02( ):
   '''True for orphan components when allow_orphans is True.
      False for orphan components when allow_orphans is False.'''

   assert componenttools.all_are_contiguous_components_in_same_thread(macros.scale(4))
   assert not componenttools.all_are_contiguous_components_in_same_thread(macros.scale(4), allow_orphans = False, 
      )


def test_componenttools_all_are_contiguous_components_in_same_thread_03( ):
   '''False for time reordered leaves in staff.'''

   t = Staff(macros.scale(4))
   assert not componenttools.all_are_contiguous_components_in_same_thread(t[2:] + t[:2], 
      )


def test_componenttools_all_are_contiguous_components_in_same_thread_04( ):
   '''False for unincorporated component.'''

   assert componenttools.all_are_contiguous_components_in_same_thread([Staff(macros.scale(4))], 
      )


def test_componenttools_all_are_contiguous_components_in_same_thread_05( ):
   '''True for empty list.'''

   assert componenttools.all_are_contiguous_components_in_same_thread([ ])
