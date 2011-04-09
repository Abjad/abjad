from abjad.tools import seqtools
from abjad.tools.pitchtools.HarmonicChromaticInterval import HarmonicChromaticInterval
from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr


def list_harmonic_chromatic_intervals_in_expr(expr):
   '''.. versionadded:: 1.1.2

   List harmonic chromatic intervals in `expr`::

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

   Return unordered set.
   '''
   
   chromatic_intervals = [ ]
   pitches = list_named_chromatic_pitches_in_expr(expr)
   unordered_pitch_pairs = seqtools.yield_all_unordered_pairs_of_sequence(pitches)
   for first_pitch, second_pitch in unordered_pitch_pairs:
      chromatic_interval_number = abs(first_pitch.numbered_chromatic_pitch) - \
         abs(second_pitch.numbered_chromatic_pitch)
      chromatic_interval = HarmonicChromaticInterval(chromatic_interval_number)
      chromatic_intervals.append(chromatic_interval)      
   
   return chromatic_intervals
