from abjad import *
import py.test


def test__ContainerDurationInterface_seconds_01( ):
   '''Container duration in seconds equals 
   sum of leaf durations in seconds.
   '''

   t = Staff(macros.scale(4))
   #t.tempo.forced = tempotools.TempoIndication(Rational(1, 4), 38)
   #t[2].tempo.forced = tempotools.TempoIndication(Rational(1, 4), 42)
   marktools.TempoMark(Rational(1, 4), 38)(t)
   marktools.TempoMark(Rational(1, 4), 42)(t[2])
   score = Score([t])

   r'''
   \new Score <<
      \new Staff {
         \tempo 4=38
         c'8
         d'8
         \tempo 4=42
         e'8
         f'8
      }
   >>
   '''

   assert score.duration.seconds == Rational(400, 133)


def test__ContainerDurationInterface_seconds_02( ):
   '''Container can not calculate duration in seconds 
      without tempo indication.'''

   t = Container(macros.scale(4))
   assert py.test.raises(UndefinedTempoError, 't.duration.seconds')
