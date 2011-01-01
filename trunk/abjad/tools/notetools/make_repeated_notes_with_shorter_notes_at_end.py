from abjad.components import Note
from abjad.tools.notetools.make_notes import make_notes
from fractions import Fraction


def make_repeated_notes_with_shorter_notes_at_end(pitch, written_duration, total_duration, prolation = Fraction(1)):
   r'''Make repeated notes with `pitch` and `written_duration` summing to `total_duration` under `prolation`::

      abjad> voice = Voice(notetools.make_repeated_notes_with_shorter_notes_at_end(0, Fraction(1, 16), Fraction(4, 16)))

   ::

      abjad> f(voice)
      \new Voice {
         c'16
         c'16
         c'16
         c'16
      }

   Fill binary remaining duration with binary notes of lesser written duration::

      abjad> voice = Voice(notetools.make_repeated_notes_with_shorter_notes_at_end(0, Fraction(1, 16), Fraction(9, 32)))

   ::

      abjad> f(voice)
      \new Voice {
         c'16
         c'16
         c'16
         c'16
         c'32
      }

   Fill nonbinary remaining duration with ad hoc tuplet::

      abjad> voice = Voice(notetools.make_repeated_notes_with_shorter_notes_at_end(0, Fraction(1, 16), Fraction(4, 10)))

   ::

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

   Return list of newly constructed components.

   .. versionchanged:: 1.1.2
      renamed ``construct.note_train( )`` to
      ``notetools.make_repeated_notes_with_shorter_notes_at_end( )``.
   '''

   prolated_duration = prolation * written_duration 
   current_duration = Fraction(0)
   result = [ ]
   while current_duration + prolated_duration <= total_duration:
      result.append(Note(pitch, written_duration))
      current_duration += prolated_duration
   remainder_duration = total_duration - current_duration
   if Fraction(0) < remainder_duration:
      multiplied_remainder = remainder_duration / prolation
      result.extend(make_notes(pitch, [multiplied_remainder]))
   return result
