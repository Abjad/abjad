from abjad.components.Chord import Chord
from abjad.components.Note import Note
from abjad.components.NoteHead import NoteHead
from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch


def is_carrier(expr):
   '''True when `expr` is an Abjad pitch, note, note-head
   of chord instance. ::

      abjad> note = Note(0, (1, 4))
      abjad> pitchtools.is_carrier(note)
      True

   Otherwise false. ::

      abjad> staff = Staff([ ])
      abjad> pitchtools.is_carrier(staff)
      False
   '''

   return isinstance(expr, (NamedPitch, Note, NoteHead, Chord))
