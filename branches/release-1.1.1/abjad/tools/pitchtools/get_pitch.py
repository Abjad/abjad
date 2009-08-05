from abjad.chord import Chord
from abjad.exceptions import ExtraPitchError
from abjad.exceptions import MissingPitchError
from abjad.note import Note
from abjad.notehead import NoteHead
from abjad.pitch import Pitch


def get_pitch(pitch_carrier):
   '''Get Abjad :class:`~abjad.pitch.pitch.Pitch` from
   Abjad :class:`~abjad.pitch.pitch.Pitch`, 
   :class:`~abjad.note.note.Note`, 
   :class:`~abjad.notehead.notehead.NoteHead` or 
   :class:`~abjad.chord.chord.Chord` instance.

   ::

      abjad> pitch = Pitch('df', 5)
      abjad> pitch
      Pitch(df, 5)
      abjad> pitchtools.get_pitch(pitch)
      Pitch(df, 5)

   ::

      abjad> note = Note(('df', 5), (1, 4))
      abjad> note
      Note(df'', 4)
      abjad> pitchtools.get_pitch(note)
      Pitch(df, 5)

   ::

      abjad> note = Note(('df', 5), (1, 4))
      abjad> note.notehead
      NoteHead(df'')
      abjad> pitchtools.get_pitch(note.notehead)
      Pitch(df, 5)

   ::

      abjad> chord = Chord([('df', 5)], (1, 4))
      abjad> chord
      Chord(df'', 4)
      abjad> pitchtools.get_pitch(chord)
      Pitch(df, 5)

   Raise :exc:`~abjad.exceptions.MissingPitchError` when
   *pitch_carrier* carries no :class:`~abjad.pitch.pitch.Pitch`.
   
   ::

      abjad> note = Note(('df', 5), (1, 4))
      abjad> note.pitch = None
      abjad> note
      Note(None, 4)
      abjad> pitchtools.get_pitch(note)
      MissingPitchError

   ::

      abjad> note = Note(('df', 5), (1, 4))
      abjad> note.pitch = None
      abjad> note.notehead
      NoteHead( )
      abjad> pitchtools.get_pitch(note.notehead)
      MissingPitchError

   ::

      abjad> chord = Chord([('df', 5)], (1, 4))
      abjad> chord.pitches = [ ]
      abjad> chord
      Chord(, 4)
      abjad> pitchtools.get_pitch(chord)
      MissingPitchError

   Raise :exc:`~abjad.exceptions.ExtraPitchError` when
   :class:`~abjad.chord.chord.Chord` carries more than one pitch.

   ::

      abjad> chord = Chord([12, 14, 23], (1, 4))
      abjad> chord
      Chord(c'' d'' b'', 4)
      abjad> pitchtools.get_pitch(chord)
      ExtraPitchError

   .. note:: 'Defective' :class:`~abjad.note.note.Note` and \
      :class:`~abjad.notehead.notehead.NoteHead` instances with \
      no :class:`~abjad.pitch.pitch.Pitch` are allowed \
      in the current implementation of Abjad but may deprecate in a future
      implementation.

   Raise :exc:`TypeError` when *pitch_carrier* is not a valid pitch carrier.

   ::

      abjad> staff = Staff([ ])
      abjad> staff
      Staff{ }
      abjad> pitchtools.get_pitch(staff)
      TypeError
   '''
   
   if isinstance(pitch_carrier, Pitch):
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
      raise TypeError('must be Pitch, Note, NoteHead or Chord.')
