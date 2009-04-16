from abjad import *
import py.test


def test_leaf_duration_interface_clock_01( ):
   '''Clock duration equals prolated duration divide by effective tempo.'''

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

   assert t[0].duration.clock == Rational(1, 76)
   assert t[1].duration.clock == Rational(1, 76)
   assert t[2].duration.clock == Rational(1, 84)
   assert t[3].duration.clock == Rational(1, 84)


def test_leaf_duration_interface_clock_02( ):
   '''Clock duration can not calculate without tempo.'''

   t = Note(0, (1, 4))
   assert py.test.raises(UndefinedTempoError, 't.duration.clock')
