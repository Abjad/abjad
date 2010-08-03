from abjad import *
import py.test


def test__SpannerReceptor_position_01( ):
   '''Return position in spanner, if spanned;
      otherwise, raise MissingSpannerError.'''

   t = Staff(macros.scale(4))
   Beam(t[2:])

   r'''
   \new Staff {
           c'8
           d'8
           e'8 [
           f'8 ]
   } 
   '''

   assert py.test.raises(MissingSpannerError, 't[0].beam.position')
   assert py.test.raises(MissingSpannerError, 't[1].beam.position')
   assert t[2].beam.position == 0
   assert t[3].beam.position == 1
