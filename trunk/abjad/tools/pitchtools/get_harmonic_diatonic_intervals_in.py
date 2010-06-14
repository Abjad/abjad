from abjad.tools import listtools
from abjad.tools.pitchtools.get_pitches import get_pitches


def get_harmonic_diatonic_intervals_in(expr):
   '''.. versionadded:: 1.1.2

   Return unordered set of diatonic intervals in `expr`. ::

      abjad> staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> pitchtools.get_harmonic_diatonic_intervals_in(staff)
      abjad> for interval in pitchtools.get_harmonic_diatonic_intervals_in(staff):
      ...     interval
      ... 
      HarmonicDiatonicInterval(minor third)
      HarmonicDiatonicInterval(minor second)
      HarmonicDiatonicInterval(major second)
      HarmonicDiatonicInterval(major third)
      HarmonicDiatonicInterval(perfect fourth)
   '''
   
   diatonic_intervals = [ ]
   pitches = get_pitches(expr)
   unordered_pitch_pairs = listtools.get_unordered_pairs(pitches)
   for first_pitch, second_pitch in unordered_pitch_pairs:
      diatonic_interval = first_pitch - second_pitch
      diatonic_interval = abs(diatonic_interval)
      diatonic_intervals.append(diatonic_interval)      
   
   return diatonic_intervals
