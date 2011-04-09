from abjad.tools import seqtools
from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr


def list_harmonic_diatonic_intervals_in_expr(expr):
   '''.. versionadded:: 1.1.2

   List harmonic diatonic intervals in `expr`::

      abjad> staff = Staff(macros.scale(4))
      abjad> pitchtools.list_harmonic_diatonic_intervals_in_expr(staff)
      abjad> for interval in pitchtools.list_harmonic_diatonic_intervals_in_expr(staff):
      ...     interval
      ... 
      HarmonicDiatonicInterval(minor third)
      HarmonicDiatonicInterval(minor second)
      HarmonicDiatonicInterval(major second)
      HarmonicDiatonicInterval(major third)
      HarmonicDiatonicInterval(perfect fourth)

   Return unordered set.
   '''
   
   diatonic_intervals = [ ]
   pitches = list_named_chromatic_pitches_in_expr(expr)
   unordered_pitch_pairs = seqtools.yield_all_unordered_pairs_of_sequence(pitches)
   for first_pitch, second_pitch in unordered_pitch_pairs:
      diatonic_interval = first_pitch - second_pitch
      diatonic_interval = abs(diatonic_interval)
      diatonic_intervals.append(diatonic_interval)      
   
   return diatonic_intervals
