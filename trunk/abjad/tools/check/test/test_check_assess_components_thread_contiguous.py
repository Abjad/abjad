from abjad import *
import py.test


def test_assess_components_thread_contiguous_01( ):
   '''True for thread contiguous components even when
      components are not strictly contiguous.'''

   t = Voice(run(4))
   t.insert(2, Voice(run(2)))
   pitchtools.diatonicize(t)

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
   assert check.assess_components([t.leaves[i] for i in outer], contiguity = 'thread')


def test_assess_components_thread_contiguous_02( ):
   '''Temporal gaps between components are OK.
      So long as gaps are filled with foreign components
      that do not belong to thread.'''

   t = Voice(run(4))
   t.insert(2, Voice(run(2)))
   Container(t[:2])
   Container(t[-2:])
   pitchtools.diatonicize(t)

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
   
   assert check.assess_components(t[0:1] + t[-1:], contiguity = 'thread')
   assert check.assess_components(t[0][:] + t[-1:], contiguity = 'thread')
   assert check.assess_components(t[0:1] + t[-1][:], contiguity = 'thread')
   assert check.assess_components(t[0][:] + t[-1][:], contiguity = 'thread')


def test_assess_components_thread_contiguous_03( ):
   '''Components that start at the same moment are bad.
      Even if components are all part of the same thread.'''

   t = Voice(run(4))
   t.insert(2, Voice(run(2)))
   Container(t[:2])
   Container(t[-2:])
   pitchtools.diatonicize(t)

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
   
   assert not check.assess_components([t, t[0]], contiguity = 'thread')
   assert not check.assess_components(t[0:1] + t[0][:], contiguity = 'thread')
   assert not check.assess_components(t[-1:] + t[-1][:], contiguity = 'thread')


def test_assess_components_thread_contiguous_04( ):
   '''True for strictly contiguous leaves in same staff.'''

   t = Staff(scale(4))
   assert check.assess_components(t[:], contiguity = 'thread')


def test_assess_components_thread_contiguous_05( ):
   '''True for orphan components when allow_orphans is True.
      False for orphan components when allow_orphans is False.'''

   assert check.assess_components(scale(4), contiguity = 'thread')
   assert not check.assess_components(scale(4), 
      contiguity = 'thread', allow_orphans = False)


def test_assess_components_thread_contiguous_06( ):
   '''False for time reordered leaves in staff.'''

   t = Staff(scale(4))
   assert not check.assess_components(t[2:] + t[:2], contiguity = 'thread')


def test_assess_components_thread_contiguous_07( ):
   '''True for unincorporated component.'''

   assert check.assess_components([Staff(scale(4))], contiguity = 'thread')


def test_assess_components_thread_contiguous_08( ):
   '''True for empty list.'''

   assert check.assess_components([ ], contiguity = 'thread')


def test_assess_components_thread_contiguous_09( ):
   '''False when components belonging to same thread are ommitted.'''

   t = Voice(scale(6))
   Beam(t[:])

   r'''\new Voice {
      c'8 [
      d'8
      e'8
      f'8
      g'8
      a'8 ]
   }'''

   assert not check.assess_components(t[:2] + t[-2:], contiguity = 'thread')


def test_assess_components_thread_contiguous_10( ):
   '''False when components belonging to same thread are ommitted.'''

   t = Voice(Container(run(2)) * 3)
   pitchtools.diatonicize(t)
   Beam(t.leaves)

   r'''\new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }'''

   assert not check.assess_components(t[:1] + t[-1:], contiguity = 'thread')
