from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch
from abjad.tools.pitchtools.list_named_pitches_in_expr import list_named_pitches_in_expr
from abjad.tools.stafftools import Clef


def suggest_clef_for_named_pitches(pitches, clefs = ['treble', 'bass']):
   '''Suggest best clef from `clefs` for `pitches` 
   as determined by minimal ledger lines. ::

      abjad> pitches = [NamedPitch(x) for x in (-30, 10, 20)]
      abjad> pitchtools.suggest_clef_for_named_pitches(pitches)
      Clef('bass')

   ::

      abjad> pitches = [NamedPitch(x) for x in (-5, 30)]
      abjad> pitchtools.suggest_clef_for_named_pitches(pitches)
      Clef('treble')

   Works for arbitrary input expression. ::

      abjad> staff = Staff(notetools.make_notes(range(-12, -6), [(1, 4)]))
      abjad> pitchtools.suggest_clef_for_named_pitches(staff)
      Clef('bass')

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.suggest_clef( )`` to
      ``pitchtools.suggest_clef_for_named_pitches( )``.
   '''

   pitches = list_named_pitches_in_expr(pitches)

   altitudes = [pitch.altitude for pitch in pitches]
   max_altitude = max(altitudes)
   min_altitude = min(altitudes)

   lowest_treble_line_pitch = NamedPitch('e', 4)
   lowest_treble_line_altitude = lowest_treble_line_pitch.altitude
   candidate_steps_below_treble = lowest_treble_line_altitude - min_altitude

   highest_bass_line_pitch = NamedPitch('a', 3)
   highest_bass_line_altitude = highest_bass_line_pitch.altitude
   candidate_steps_above_bass = max_altitude - highest_bass_line_altitude

   if candidate_steps_above_bass < candidate_steps_below_treble:
      return Clef('bass')
   else:
      return Clef('treble')
