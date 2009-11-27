from abjad.tools import listtools
from abjad.tools.pitchtools.get_pitches import get_pitches


def get_diatonic_intervals_in(expr):
   '''.. versionadded:: 1.1.2

   Return unordered set of diatonic intervals in `expr`. ::

      abjad> staff = Staff(construct.scale(4))
      abjad> pitchtools.get_diatonic_intervals_in(staff)
      abjad> for interval in pitchtools.get_diatonic_intervals_in(staff):
      ...     interval
      ... 
      DiatonicInterval(ascending major third)
      DiatonicInterval(ascending major second)
      DiatonicInterval(ascending major second)
      DiatonicInterval(ascending perfect fourth)
      DiatonicInterval(ascending minor third)
      DiatonicInterval(ascending minor second)
   '''
   
   diatonic_intervals = set([ ])
   pitches = get_pitches(expr)
   unordered_pitch_pairs = listtools.get_unordered_pairs(pitches)
   for unordered_pitch_pair in unordered_pitch_pairs:
      first_pitch = unordered_pitch_pair.pop( )
      second_pitch = unordered_pitch_pair.pop( )
      diatonic_interval = first_pitch - second_pitch
      diatonic_interval = abs(diatonic_interval)
      diatonic_intervals.add(diatonic_interval)      
   
   return diatonic_intervals
