from abjad import *
import py.test


def test__LeafDurationInterface_seconds_01( ):
   '''Clock duration equals prolated duration divide by effective tempo.'''

   #t = Container(macros.scale(4))
   t = Staff(macros.scale(4))
   contexttools.TempoMark(Fraction(1, 4), 38)(t)
   contexttools.TempoMark(Fraction(1, 4), 42)(t[2])
   Score([t])

   r'''
   \new Staff {
      \tempo 4=38
      c'8
      d'8
      \tempo 4=42
      e'8
      f'8
   }
   '''

   assert t[0].duration.seconds == Fraction(15, 19)
   assert t[1].duration.seconds == Fraction(15, 19)
   assert t[2].duration.seconds == Fraction(5, 7)
   assert t[3].duration.seconds == Fraction(5, 7)


def test__LeafDurationInterface_seconds_02( ):
   '''Clock duration can not calculate without tempo.'''

   t = Note(0, (1, 4))
   assert py.test.raises(MissingTempoError, 't.duration.seconds')
