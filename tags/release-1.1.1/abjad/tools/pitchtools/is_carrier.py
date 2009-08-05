from abjad.chord import Chord
from abjad.note import Note
from abjad.notehead import NoteHead
from abjad.pitch import Pitch


def is_carrier(expr):
   '''``True`` when *expr* is an Abjad Pitch, Note, Notehead or
   Chord instance, otherwise ``False``.

   ::

      abjad> note = Note(0, (1, 4))
      abjad> pitchtools.is_carrier(note)
      True

   ::

      abjad> staff = Staff([ ])
      abjad> pitchtools.is_carrier(staff)
      False'''

   return isinstance(expr, (Pitch, Note, NoteHead, Chord))
