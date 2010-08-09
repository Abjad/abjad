from abjad.tools import listtools
from abjad.tools.pitchtools.get_pitches import get_pitches


def list_harmonic_diatonic_intervals_in_expr(expr):
   '''.. versionadded:: 1.1.2

   Return unordered set of diatonic intervals in `expr`. ::

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

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.get_harmonic_diatonic_intervals_in( )`` to
      ``pitchtools.list_harmonic_diatonic_intervals_in_expr( )``.
   '''
   
   diatonic_intervals = [ ]
   pitches = get_pitches(expr)
   unordered_pitch_pairs = listtools.get_unordered_pairs(pitches)
   for first_pitch, second_pitch in unordered_pitch_pairs:
      diatonic_interval = first_pitch - second_pitch
      diatonic_interval = abs(diatonic_interval)
      diatonic_intervals.append(diatonic_interval)      
   
   return diatonic_intervals
