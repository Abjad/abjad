from abjad import *


def test_spanner_getitem_01( ):
   '''Get at nonnegative index in spanner.'''

   t = Voice(Container(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[:])

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

   assert p[0] is t[0]


def test_spanner_getitem_02( ):
   '''Get at negative index in spanner.'''

   t = Voice(Container(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[:])

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

   assert p[-1] is t[-1]


def test_spanner_getitem_03( ):
   '''Get slice from spanner.'''

   t = Voice(Container(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[:])

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

   assert p[-2:] == t[-2:]


def test_spanner_getitem_04( ):
   '''Get all spanner components.
      Equivalent to p.clear( ).'''

   t = Voice(Container(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[:])

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

   assert p[:] == t[:]
