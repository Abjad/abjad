from abjad import *
import py.test


def test_offset_seconds_01( ):
   '''Offset seconds can not calculate without excplit tempo indication.'''

   t = Staff(construct.scale(4))
   
   r'''\new Staff {
      c'8
      d'8
      e'8
      f'8
   }'''

   assert py.test.raises(UndefinedTempoError, 't[0].offset.seconds.start')
   assert py.test.raises(UndefinedTempoError, 't[0].offset.seconds.stop')


def test_offset_seconds_02( ):
   '''Offset seconds work with explicit tempo indication.'''

   t = Staff(construct.scale(4))
   t.tempo.forced = TempoIndication(Rational(1, 8), 48)
   
   r'''\new Staff {
      \tempo 8=48
      c'8
      d'8
      e'8
      f'8
   }'''

   assert t[0].offset.seconds.start == Rational(0)
   assert t[1].offset.seconds.start == Rational(5, 4)
