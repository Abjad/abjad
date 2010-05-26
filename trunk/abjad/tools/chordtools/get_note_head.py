from abjad.chord import Chord
from abjad.exceptions import ExtraNoteHeadError
from abjad.exceptions import MissingNoteHeadError
from abjad.pitch import Pitch
from abjad.rational import Rational


def get_note_head(chord, pitch):
   '''Return note head with `pitch` in `chord`.

   Set `pitch` to an Abjad pitch instance or a number. ::

      abjad> chord = Chord([12, 14, 23], Rational(1, 4))
      abjad> chordtools.get_note_head(chord, 14)
      NoteHead('d', 5)

   Raise missing note head error when `chord` contains no 
   note head with pitch equal to `pitch`. ::

      abjad> chord = Chord([12, 14, 23], Rational(1, 4))
      abjad> chordtools.get_note_head(chord, 14)
      MissingNoteHeadError

   Raise extra note head error when `chord` contains more than 
   one note head with pitch equal to `pitch`. ::

      abjad> chord = Chord([12, 12], Rational(1, 4))
      abjad> chordtools.get_note_head(chord, 12)
      ExtraNoteHeadError
   '''

   if not isinstance(chord, Chord):
      raise ValueError('must be Abjad chord.')

   if not isinstance(pitch, (Pitch, int, float, long, Rational)):
      raise ValueError('must be number or Abjad pitch.')

   result = [ ]
   
   if isinstance(pitch, Pitch):
      for note_head in chord.note_heads:
         if note_head.pitch == pitch:
            result.append(note_head)
   else:
      for note_head in chord.note_heads:
         if note_head.pitch.number == pitch:
            result.append(note_head)

   count = len(result)

   if count == 0:
      raise MissingNoteHeadError
   elif count == 1:
      note_head = result[0]
      return note_head
   else:
      raise ExtraNoteHeadError
