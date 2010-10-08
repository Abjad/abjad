from abjad.components.Note import Note
from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch
from abjad.tools.pitchtools.TwelveToneRow import TwelveToneRow


def permute_named_chromatic_pitch_carrier_list_by_twelve_tone_row(pitches, row):
   '''Permute `pitches` by `row`. 
   
   ::

      abjad> notes = notetools.make_notes([17, -10, -2, 11], [Fraction(1, 4)])
      abjad> row = pitchtools.TwelveToneRow([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
      abjad> pitchtools.permute_named_chromatic_pitch_carrier_list_by_twelve_tone_row(notes, row)
      [Note(bf, 4), Note(d, 4), Note(f'', 4), Note(b', 4)]

   This function works by reference only. No objects are cloned.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.permute_by_row( )`` to
      ``pitchtools.permute_named_chromatic_pitch_carrier_list_by_twelve_tone_row( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.permute_pitch_list_by_twelve_tone_row( )`` to
      ``pitchtools.permute_named_chromatic_pitch_carrier_list_by_twelve_tone_row( )``.
   '''

   if not isinstance(row, TwelveToneRow):
      raise TypeError('must be twelve-tone row.')

   result = [ ] 

   for pc in row:
      matching_pitches = [ ]
      for pitch in pitches:
         if isinstance(pitch, NamedPitch):
            if pitch.numeric_pitch_class == pc:   
               matching_pitches.append(pitch)
         elif isinstance(pitch, Note):
            if pitch.pitch.numeric_pitch_class == pc:
               matching_pitches.append(pitch)
         else:
            raise TypeError('must be Abjad Pitch or Note.')
      result.extend(matching_pitches)

   return result
