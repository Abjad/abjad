from abjad.helpers.are_thread_contiguous_components import _are_thread_contiguous_components
from abjad import *
import py.test


def test_are_thread_contiguous_components_01( ):
   '''True for thread contiguous components even when
      components are not strictly contiguous.'''

   t = Voice(run(4))
   t.insert(2, Voice(run(2)))
   diatonicize(t)

   r'''\new Voice {
      c'8
      d'8
      \new Voice {
         e'8
         f'8
      }
      g'8
      a'8
   }'''

   outer = (0, 1, 4, 5)
   assert _are_thread_contiguous_components([t.leaves[i] for i in outer])


def test_are_thread_contiguous_components_02( ):
   '''Temporal gaps between components are OK.
      So long as gaps are filled with foreign components
      that do not belong to thread.'''

   t = Voice(run(4))
   t.insert(2, Voice(run(2)))
   Sequential(t[:2])
   Sequential(t[-2:])
   diatonicize(t)

   r'''\new Voice {
      {
         c'8
         d'8
      }
      \new Voice {
         e'8
         f'8
      }
      {
         g'8
         a'8
      }
   }'''
   
   assert _are_thread_contiguous_components(t[0:1] + t[-1:])
   assert _are_thread_contiguous_components(t[0][:] + t[-1:])
   assert _are_thread_contiguous_components(t[0:1] + t[-1][:])
   assert _are_thread_contiguous_components(t[0][:] + t[-1][:])


def test_are_thread_contiguous_components_03( ):
   '''Components that start at the same moment are bad.
      Even if components are all part of the same thread.'''

   t = Voice(run(4))
   t.insert(2, Voice(run(2)))
   Sequential(t[:2])
   Sequential(t[-2:])
   diatonicize(t)

   r'''\new Voice {
      {
         c'8
         d'8
      }
      \new Voice {
         e'8
         f'8
      }
      {
         g'8
         a'8
      }
   }'''
   
   assert not _are_thread_contiguous_components([t, t[0]])
   assert not _are_thread_contiguous_components(t[0:1] + t[0][:])
   assert not _are_thread_contiguous_components(t[-1:] + t[-1][:])


def test_are_thread_contiguous_components_04( ):
   '''True for strictly contiguous leaves in same staff.'''

   t = Staff(scale(4))
   assert _are_thread_contiguous_components(t[:])


def test_are_thread_contiguous_components_05( ):
   '''False for unincorporated components.'''

   assert not _are_thread_contiguous_components(scale(4))


def test_are_thread_contiguous_components_06( ):
   '''False for time reordered leaves in staff.'''

   t = Staff(scale(4))
   assert not _are_thread_contiguous_components(t[2:] + t[:2])


def test_are_thread_contiguous_components_07( ):
   '''False for unincorporated component.'''

   py.test.skip('TODO: Active proposal that staves and staff groups should not thread. Outcome of that proposal will determine the behavior of this test.')
   assert not _are_thread_contiguous_components(
      [Staff(scale(4))])


def test_are_thread_contiguous_components_08( ):
   '''True for empty list.'''

   assert _are_thread_contiguous_components([ ])
