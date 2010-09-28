from abjad import *


def test__SpannerDurationInterface_seconds_01( ):
   '''Spanner duration in seconds equals sum of duration
      of all leaves in spanner, in seconds.'''

   t = Voice([Measure((2, 12), macros.scale(2)), 
      Measure((2, 8), macros.scale(2))])
   marktools.TempoMark(Fraction(1, 8), 42, target_context = Voice)(t)
   beam = spannertools.BeamSpanner(t.leaves)
   crescendo = spannertools.CrescendoSpanner(t[0][:])
   decrescendo = spannertools.DecrescendoSpanner(t[1][:])

   r'''
   \new Voice {
            \tempo 8=42
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

   assert beam.duration.seconds == Fraction(100, 21)
   assert crescendo.duration.seconds == Fraction(40, 21)
   assert decrescendo.duration.seconds == Fraction(20, 7)
