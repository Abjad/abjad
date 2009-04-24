from abjad import *


def test_durtools_within_seconds_01( ):
   '''True when split point is within duration of component, in seconds.'''

   t = Note(0, (1, 4))
   t.tempo.forced = TempoIndication(Rational(1, 2), 60)

   assert durtools.within_seconds(0, t)
   assert durtools.within_seconds(0.1, t)
   assert durtools.within_seconds(0.333, t)
   assert not durtools.within_seconds(0.5, t)
