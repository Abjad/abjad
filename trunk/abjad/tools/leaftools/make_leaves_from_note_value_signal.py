from abjad.components import Note
from abjad.components import Rest


def make_leaves_from_note_value_signal(note_value_signal, unit_of_signal):
   '''.. versionadded:: 1.1.2

   Make leaves from `note_value_signal` and `unit_of_signal`::

      abjad> leaftools.make_leaves_from_note_value_signal([2, -2, 3, -3], Fraction(1, 8))
      [Note("c'4"), Rest('r4'), Note("c'4."), Rest('r4.')]

   Interpret positive elements in `note_value_signal` as notes.

   Interpret negative elements in `note_value_signal` as rests.

   Set the pitch of all notes to middle C.

   Return list of notes and / or rests.
   '''

   result = [ ]

   for note_value in note_value_signal:
      if note_value == 0:
         raise ValueError('note values must be nonzero.')
      elif 0 < note_value:
         leaf = Note(0, note_value * unit_of_signal)
      else:
         leaf = Rest(-note_value * unit_of_signal)
      result.append(leaf)

   return result
