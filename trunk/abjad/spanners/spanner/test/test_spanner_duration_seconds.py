from abjad import *


def test_spanner_duration_seconds_01( ):
   '''Spanner duration in seconds equals sum of duration
      of all leaves in spanner, in seconds.'''

   t = Voice([RigidMeasure((2, 12), construct.scale(2)), 
      RigidMeasure((2, 8), construct.scale(2))])
   t.tempo.forced = TempoIndication(Rational(1, 8), 42)
   beam = Beam(t.leaves)
   crescendo = Crescendo(t[0][:])
   decrescendo = Decrescendo(t[1][:])

   r'''\new Voice {
            \tempo 8=42
                   \time 2/12
                   \scaleDurations #'(2 . 3) {
                           c'8 [ \<
                           d'8 \!
                   }
                   \time 2/8
                   c'8 \>
                   d'8 ] \!
   }'''

   assert beam.duration.seconds == Rational(100, 21)
   assert crescendo.duration.seconds == Rational(40, 21)
   assert decrescendo.duration.seconds == Rational(20, 7)
