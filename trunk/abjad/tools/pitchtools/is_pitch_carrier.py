from abjad.components.Chord import Chord
from abjad.components.Note import Note
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch


def is_pitch_carrier(expr):
   '''True when `expr` is an Abjad pitch, note, note-head
   of chord instance. ::

      abjad> note = Note(0, (1, 4))
      abjad> pitchtools.is_pitch_carrier(note)
      True

   Otherwise false. ::

      abjad> staff = Staff([ ])
      abjad> pitchtools.is_pitch_carrier(staff)
      False

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.is_carrier( )`` to
      ``pitchtools.is_pitch_carrier( )``.
   '''

   from abjad.tools.notetools.NoteHead import NoteHead
   return isinstance(expr, (NamedChromaticPitch, Note, NoteHead, Chord))
