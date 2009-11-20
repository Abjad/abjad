from abjad.note import Note
from abjad.pitch import Pitch


def permute_by_row(pitches, row):
   '''Permute `pitches` by `row`. 
   
   ::

      abjad> notes = [Note(p, (1, 4)) for p in (17, -10, -2, 11)]
      abjad> row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
      abjad> pitchtools.permute_by_row(notes, row)
      [Note(bf, 4), Note(d, 4), Note(f'', 4), Note(b', 4)]

   This function works by reference only. No objects are cloned.
   '''

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
