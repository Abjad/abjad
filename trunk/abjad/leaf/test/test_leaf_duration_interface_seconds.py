from abjad import *
import py.test


def test_leaf_duration_interface_seconds_01( ):
   '''Clock duration equals prolated duration divide by effective tempo.'''

   t = Container(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   t.tempo.forced = tempotools.TempoIndication(Rational(1, 4), 38)
   t[2].tempo.forced = tempotools.TempoIndication(Rational(1, 4), 42)

   r'''
   {
      \tempo 4=38
      c'8
      d'8
      \tempo 4=42
      e'8
      f'8
   }
   '''

   assert t[0].duration.seconds == Rational(15, 19)
   assert t[1].duration.seconds == Rational(15, 19)
   assert t[2].duration.seconds == Rational(5, 7)
   assert t[3].duration.seconds == Rational(5, 7)


def test_leaf_duration_interface_seconds_02( ):
   '''Clock duration can not calculate without tempo.'''

   t = Note(0, (1, 4))
   assert py.test.raises(UndefinedTempoError, 't.duration.seconds')
