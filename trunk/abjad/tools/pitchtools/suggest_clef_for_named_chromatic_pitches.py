from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch
from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr
from abjad.tools import contexttools


def suggest_clef_for_named_chromatic_pitches(pitches, clefs = ['treble', 'bass']):
   '''Suggest best clef from `clefs` for `pitches` 
   as determined by minimal ledger lines. ::

      abjad> pitches = [NamedPitch(x) for x in (-30, 10, 20)]
      abjad> pitchtools.suggest_clef_for_named_chromatic_pitches(pitches)
      ClefMark('bass')

   ::

      abjad> pitches = [NamedPitch(x) for x in (-5, 30)]
      abjad> pitchtools.suggest_clef_for_named_chromatic_pitches(pitches)
      ClefMark('treble')

   Works for arbitrary input expression. ::

      abjad> staff = Staff(notetools.make_notes(range(-12, -6), [(1, 4)]))
      abjad> pitchtools.suggest_clef_for_named_chromatic_pitches(staff)
      ClefMark('bass')

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.suggest_clef( )`` to
      ``pitchtools.suggest_clef_for_named_chromatic_pitches( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.suggest_clef_for_named_pitches( )`` to
      ``pitchtools.suggest_clef_for_named_chromatic_pitches( )``.
   '''

   pitches = list_named_chromatic_pitches_in_expr(pitches)

   diatonic_pitch_numbers = [pitch.diatonic_pitch_number for pitch in pitches]
   max_diatonic_pitch_number = max(diatonic_pitch_numbers)
   min_diatonic_pitch_number = min(diatonic_pitch_numbers)

   lowest_treble_line_pitch = NamedPitch('e', 4)
   lowest_treble_line_diatonic_pitch_number = lowest_treble_line_pitch.diatonic_pitch_number
   candidate_steps_below_treble = \
      lowest_treble_line_diatonic_pitch_number - min_diatonic_pitch_number

   highest_bass_line_pitch = NamedPitch('a', 3)
   highest_bass_line_diatonic_pitch_number = highest_bass_line_pitch.diatonic_pitch_number
   candidate_steps_above_bass = max_diatonic_pitch_number - highest_bass_line_diatonic_pitch_number

   if candidate_steps_above_bass < candidate_steps_below_treble:
      return contexttools.ClefMark('bass')
   else:
      return contexttools.ClefMark('treble')
