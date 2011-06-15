from abjad import *


def test__SpannerDurationInterface_prolated_01( ):
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

   assert beam.duration.prolated == Duration(5, 12)
   assert crescendo.duration.prolated == Duration(2, 12)
   assert decrescendo.duration.prolated == Duration(2, 8)
