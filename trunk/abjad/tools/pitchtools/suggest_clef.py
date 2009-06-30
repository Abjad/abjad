from abjad.clef import Clef
from abjad.pitch import Pitch


def suggest_clef(pitches, clefs = ['treble', 'bass']):
   '''Suggest best clef for `pitches` determined by the least number
   of leger lines required to notate all pitches on a single staff. ::

      abjad> pitches = [Pitch(x) for x in (-30, 10, 20)]
      abjad> pitchtools.suggest_clef(pitches)
      Clef('bass')

   ::

      abjad> pitches = [Pitch(x) for x in (-5, 30)]
      abjad> pitchtools.suggest_clef(pitches)
      Clef('treble')
   '''

   assert isinstance(pitches, list)
   assert all([isinstance(pitch, Pitch) for pitch in pitches])

   altitudes = [pitch.altitude for pitch in pitches]
   max_altitude = max(altitudes)
   min_altitude = min(altitudes)

   lowest_treble_line_pitch = Pitch('e', 4)
   lowest_treble_line_altitude = lowest_treble_line_pitch.altitude
   candidate_steps_below_treble = lowest_treble_line_altitude - min_altitude

   highest_bass_line_pitch = Pitch('a', 3)
   highest_bass_line_altitude = highest_bass_line_pitch.altitude
   candidate_steps_above_bass = max_altitude - highest_bass_line_altitude

   if candidate_steps_above_bass < candidate_steps_below_treble:
      return Clef('bass')
   else:
      return Clef('treble')
