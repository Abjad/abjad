from abjad import *


def test_spanner_offset_stop_01( ):
   '''Return stop time of spanner in score.'''

   t = Voice(macros.scale(4))
   beam = Beam(t[1:3])
   glissando = Glissando([t])

   r'''
   \new Voice {
           c'8 \glissando
           d'8 [ \glissando
           e'8 ] \glissando
           f'8
   }
   '''

   assert beam.offset.stop == Rational(3, 8)
   assert glissando.offset.stop == Rational(4, 8)
