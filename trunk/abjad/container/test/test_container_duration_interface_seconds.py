from abjad import *
import py.test


def test_container_duration_interface_seconds_01( ):
   '''Container duration in seconds equals 
      sum of leaf durations in seconds.'''

   t = Container(macros.scale(4))
   t.tempo.forced = tempotools.TempoIndication(Rational(1, 4), 38)
   t[2].tempo.forced = tempotools.TempoIndication(Rational(1, 4), 42)

   r'''
   {
      \tempo 8=38
      c'8
      d'8
      \tempo 8=42
      e'8
      f'8
   }
   '''

   assert t.duration.seconds == Rational(400, 133)


def test_container_duration_interface_seconds_02( ):
   '''Container can not calculate duration in seconds 
      without tempo indication.'''

   t = Container(macros.scale(4))
   assert py.test.raises(UndefinedTempoError, 't.duration.seconds')
