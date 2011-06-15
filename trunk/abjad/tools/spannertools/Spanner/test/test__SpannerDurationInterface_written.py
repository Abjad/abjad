from abjad import *


def test__SpannerDurationInterface_written_01( ):
   t = Voice([Measure((2, 12), "c'8 d'8"), 
      Measure((2, 8), "c'8 d'8")])
   beam = spannertools.BeamSpanner(t.leaves)
   crescendo = spannertools.CrescendoSpanner(t[0][:])
   decrescendo = spannertools.DecrescendoSpanner(t[1][:])

   r'''
   \new Voice {
                   \time 2/12
                   \scaleDurations #'(2 . 3) {
                           c'8 [ \<
                           d'8 \!
                   }
                   \time 2/8
                   c'8 \>
                   d'8 ] \!
   }
   '''

   assert beam.duration.written == Duration(4, 8)
   assert crescendo.duration.written == Duration(2, 8)
   assert decrescendo.duration.written == Duration(2, 8)
