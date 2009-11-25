from abjad.note import Note
from abjad.pitch import Pitch
from abjad.tools.pitchtools.TwelveToneRow import TwelveToneRow


def permute_by_row(pitches, row):
   '''Permute `pitches` by `row`. 
   
   ::

      abjad> notes = construct.notes([17, -10, -2, 11], [Rational(1, 4)])
      abjad> row = pitchtools.TwelveToneRow([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
      abjad> pitchtools.permute_by_row(notes, row)
      [Note(bf, 4), Note(d, 4), Note(f'', 4), Note(b', 4)]

   This function works by reference only. No objects are cloned.
   '''

   if not isinstance(row, TwelveToneRow):
      raise TypeError('must be twelve-tone row.')

   result = [ ] 

   for pc in row:
      matching_pitches = [ ]
      for pitch in pitches:
         if isinstance(pitch, Pitch):
            if pitch.pc == pc:   
               matching_pitches.append(pitch)
         elif isinstance(pitch, Note):
            if pitch.pitch.pc == pc:
               matching_pitches.append(pitch)
         else:
            raise TypeError('must be Abjad Pitch or Note.')
      result.extend(matching_pitches)

   return result
