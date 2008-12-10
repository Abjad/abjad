from abjad import *
import py.test


py.test.skip('Tests for spanned containers development.')

def test_span_differently_named_01( ):
   '''Spanners refuse differently named containers.'''
   v1 = Voice([Note(i, (1,8)) for i in range(4)])
   v1.invocation.name = 'yourvoice'
   v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   v2.invocation.name = 'myvoice'
   t = Staff([v1, v2])
   assert py.test.raises(ContiguityError, 'Beam(t)')
   assert py.test.raises(ContiguityError, 'Beam(t[ : ])')
   r'''
   \new Staff {
      \context Voice = "yourvoice" {
         c'8
         cs'8
         d'8
         ef'8
      }
      \context Voice = "myvoice" {
         e'8
         f'8
         fs'8
         g'8
      }
   }
   '''


def test_span_differently_named_02( ):
   '''Spanners refuse differently named containers.'''
   vl1 = Voice([Note(i, (1,8)) for i in range(4)])
   vl1.invocation.name = 'low'
   vl1.invocation.command = 'context'
   vl2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   vl2.invocation.name = 'low'
   vl2.invocation.command = 'context'
   vh1 = Voice([Note(i, (1,8)) for i in range(12,16)])
   vh1.invocation.name = 'high'
   vh1.invocation.command = 'context'
   vh2 = Voice([Note(i, (1,8)) for i in range(16,20)])
   vh2.invocation.name = 'high'
   vh2.invocation.command = 'context'
   s1 = Staff([vh1, vl1])
   s1.invocation.name = 'mystaff'
   s1.invocation.command = 'context'
   s1.brackets = 'double-angle'
   s2 = Staff([vl2, vh2])
   s2.invocation.name = 'mystaff'
   s2.invocation.command = 'context'
   s2.brackets = 'double-angle'
   seq = Sequential([s1, s2])
   assert py.test.raises(ContiguityError, 'Beam(seq)')
   assert py.test.raises(ContiguityError, 'Beam(seq[0])')
   assert py.test.raises(ContiguityError, 'Beam(seq[1])')
   r'''
   {
      \context Staff = "mystaff" <<
         \context Voice = "high" {
            c''8
            cs''8
            d''8
            ef''8
         }
         \context Voice = "low" {
            c'8
            cs'8
            d'8
            ef'8
         }
      >>
      \context Staff = "mystaff" <<
         \context Voice = "low" {
            e'8
            f'8
            fs'8
            g'8
         }
         \context Voice = "high" {
            e''8
            f''8
            fs''8
            g''8
         }
      >>
   }
   '''

