from abjad.chord import Chord
from abjad.exceptions import ExtraNoteHeadError
from abjad.exceptions import MissingNoteHeadError
from abjad.pitch.pitch import Pitch
from abjad.rational import Rational


def get_notehead(chord, pitch):
   '''Return notehead with `pitch` in `chord`.
   Set `pitch` to an Abjad :class:`~abjad.pitch.pitch.Pitch`
   instance or a number. ::

      abjad> chord = Chord([12, 14, 23], Rational(1, 4))
      abjad> chordtools.get_notehead(chord, 14)
      NoteHead('d', 5)

   Raise :exc:`~abjad.exceptions.exceptions.MissingNoteHeadError`
   when `chord` contains no notehead with pitch equal to `pitch`. ::

      abjad> chord = Chord([12, 14, 23], Rational(1, 4))
      abjad> chordtools.get_notehead(chord, 14)
      MissingNoteHeadError

   Raise :exc:`~abjad.exceptions.exceptions.ExtraNoteHeadError`
   when `chord` contains more than one notehead with pitch equal to `pitch`. ::

      abjad> chord = Chord([12, 12], Rational(1, 4))
      abjad> chordtools.get_notehead(chord, 12)
      ExtraNoteHeadError
   '''

   if not isinstance(chord, Chord):
      raise ValueError('must be Abjad chord.')

   if not isinstance(pitch, (Pitch, int, float, long, Rational)):
      raise ValueError('must be number or Abjad pitch.')

   result = [ ]
   
   if isinstance(pitch, Pitch):
      for notehead in chord.noteheads:
         if notehead.pitch == pitch:
            result.append(notehead)
   else:
      for notehead in chord.noteheads:
         if notehead.pitch.number == pitch:
            result.append(notehead)

   count = len(result)

   if count == 0:
      raise MissingNoteHeadError
   elif count == 1:
      notehead = result[0]
      return notehead
   else:
      raise ExtraNoteHeadError
