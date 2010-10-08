from abjad.tools import listtools
from abjad.tools.pitchtools.HarmonicChromaticInterval import HarmonicChromaticInterval
from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr


def list_harmonic_chromatic_intervals_in_expr(expr):
   '''.. versionadded:: 1.1.2

   Return unordered set of harmonic chromatic intervals in `expr`. ::

      abjad> staff = Staff(macros.scale(4))
      abjad> pitchtools.list_harmonic_chromatic_intervals_in_expr(staff)
      abjad> for interval in pitchtools.list_harmonic_chromatic_intervals_in_expr(staff):
      ...     interval
      ... 
      HarmonicChromaticInterval(4)
      HarmonicChromaticInterval(2)
      HarmonicChromaticInterval(5)
      HarmonicChromaticInterval(2)
      HarmonicChromaticInterval(3)
      HarmonicChromaticInterval(1)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.get_harmonic_chromatic_intervals_in( )`` to
      ``pitchtools.list_harmonic_chromatic_intervals_in_expr( )``.
   '''
   
   chromatic_intervals = [ ]
   pitches = list_named_chromatic_pitches_in_expr(expr)
   unordered_pitch_pairs = listtools.get_unordered_pairs(pitches)
   for first_pitch, second_pitch in unordered_pitch_pairs:
      chromatic_interval_number = abs(first_pitch.numbered_chromatic_pitch._chromatic_pitch_number - second_pitch.numbered_chromatic_pitch._chromatic_pitch_number)
      chromatic_interval = HarmonicChromaticInterval(chromatic_interval_number)
      chromatic_intervals.append(chromatic_interval)      
   
   return chromatic_intervals
