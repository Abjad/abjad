from abjad.components.Chord import Chord
from abjad.exceptions import ExtraPitchError
from abjad.exceptions import MissingPitchError
from abjad.components.Note import Note
from abjad.components.NoteHead import NoteHead
from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch


def get_pitch(pitch_carrier):
   '''Get Abjad pitch instance from pitch, note, note head
   of chord `pitch_carrier`. ::

      abjad> pitch = NamedPitch('df', 5)
      abjad> pitch
      NamedPitch(df, 5)
      abjad> pitchtools.get_pitch(pitch)
      NamedPitch(df, 5)

   ::

      abjad> note = Note(('df', 5), (1, 4))
      abjad> note
      Note(df'', 4)
      abjad> pitchtools.get_pitch(note)
      NamedPitch(df, 5)

   ::

      abjad> note = Note(('df', 5), (1, 4))
      abjad> note.note_head
      NoteHead(df'')
      abjad> pitchtools.get_pitch(note.note_head)
      NamedPitch(df, 5)

   ::

      abjad> chord = Chord([('df', 5)], (1, 4))
      abjad> chord
      Chord(df'', 4)
      abjad> pitchtools.get_pitch(chord)
      NamedPitch(df, 5)

   Raise :exc:`~abjad.exceptions.MissingPitchError` when
   `pitch_carrier` carries no pitch. ::

      abjad> note = Note(('df', 5), (1, 4))
      abjad> note.pitch = None
      abjad> note
      Note(None, 4)
      abjad> pitchtools.get_pitch(note)
      MissingPitchError

   ::

      abjad> note = Note(('df', 5), (1, 4))
      abjad> note.pitch = None
      abjad> note.note_head
      NoteHead( )
      abjad> pitchtools.get_pitch(note.note_head)
      MissingPitchError

   ::

      abjad> chord = Chord([('df', 5)], (1, 4))
      abjad> chord.pitches = [ ]
      abjad> chord
      Chord(, 4)
      abjad> pitchtools.get_pitch(chord)
      MissingPitchError

   Raise :exc:`~abjad.exceptions.ExtraPitchError` when
   chord carries more than one pitch. ::

      abjad> chord = Chord([12, 14, 23], (1, 4))
      abjad> chord
      Chord(c'' d'' b'', 4)
      abjad> pitchtools.get_pitch(chord)
      ExtraPitchError

   .. note:: 'Defective' note and note head instances with no
      pitch are allowed 
      in the current implementation of Abjad but may deprecate in a future
      implementation.

   Raise :exc:`TypeError` when `pitch_carrier` is not a valid pitch carrier. ::

      abjad> staff = Staff([ ])
      abjad> staff
      Staff{ }
      abjad> pitchtools.get_pitch(staff)
      TypeError
   '''
   
   if isinstance(pitch_carrier, NamedPitch):
      return pitch_carrier
   elif isinstance(pitch_carrier, Note):
      pitch = pitch_carrier.pitch
      if pitch is not None:
         return get_pitch(pitch)
      else:
         raise MissingPitchError
   elif isinstance(pitch_carrier, NoteHead):
      pitch = pitch_carrier.pitch
      if pitch is not None:
         return get_pitch(pitch)
      else:
         raise MissingPitchError
   elif isinstance(pitch_carrier, Chord):
      pitches = pitch_carrier.pitches
      if len(pitches) == 0:
         raise MissingPitchError
      elif len(pitches) == 1:
         return get_pitch(pitches[0])
      else:
         raise ExtraPitchError
   else:
      raise TypeError(
         '%s must be Pitch, Note, NoteHead or Chord.' % pitch_carrier)
