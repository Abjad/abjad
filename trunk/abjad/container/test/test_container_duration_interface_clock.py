from abjad import *
import py.test


def test_container_duration_interface_clock_01( ):
   '''Clock duration equals sum of leaf clock durations.'''

   t = Container(construct.scale(4))
   t.tempo.forced = TempoIndication(Rational(1, 4), 38)
   t[2].tempo.forced = TempoIndication(Rational(1, 4), 42)

   r'''{
      \tempo 8=38
      c'8
      d'8
      \tempo 8=42
      e'8
      f'8
   }'''

   assert t.duration.clock == Rational(20, 399)


def test_container_duration_interface_clock_02( ):
   '''Clock duration can not calculate without tempo.'''

   t = Container(construct.scale(4))
   assert py.test.raises(UndefinedTempoError, 't.duration.clock')
