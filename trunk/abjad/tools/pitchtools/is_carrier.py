from abjad.chord.chord import Chord
from abjad.pitch.pitch import Pitch
from abjad.note.note import Note
from abjad.notehead.notehead import NoteHead


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
