from abjad.note import Note
from abjad.rational import Rational
from abjad.tools.construct.notes import notes


def note_train(pitch, written_duration, total_duration, 
   prolation = Rational(1)):
   r'''Construct notes with `pitch` and `written_duration`
   summing to `total_duration` under `prolation`::

      abjad> voice = Voice(construct.note_train(0, Rational(1, 16), Rational(4, 16)))
      abjad> f(voice)
      \new Voice {
         c'16
         c'16
         c'16
         c'16
      }

   Fill binary remaining duration with binary notes 
   of lesser written duration::

      abjad> voice = Voice(construct.note_train(0, Rational(1, 16), Rational(9, 32)))
      abjad> f(voice)
      \new Voice {
         c'16
         c'16
         c'16
         c'16
         c'32
      }

   Fill nonbinary remaining duration with ad hoc tuplet::

      abjad> voice = Voice(construct.note_train(0, Rational(1, 16), Rational(4, 10)))
      abjad> f(voice)
      \new Voice {
         c'16
         c'16
         c'16
         c'16
         c'16
         c'16
         \times 4/5 {
            c'32
         }
      }

   Set `prolation` when constructing notes in a nonbinary measure.
   '''

   prolated_duration = prolation * written_duration 
   current_duration = Rational(0)
   result = [ ]
   while current_duration + prolated_duration <= total_duration:
      result.append(Note(pitch, written_duration))
      current_duration += prolated_duration
   remainder_duration = total_duration - current_duration
   if remainder_duration > Rational(0):
      multiplied_remainder = ~prolation * remainder_duration
      result.extend(notes(pitch, [multiplied_remainder]))
   return result
