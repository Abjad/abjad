from abjad.tools import listtools
from abjad.tools.pitchtools.ChromaticInterval import ChromaticInterval
from abjad.tools.pitchtools.get_pitches import get_pitches


def get_chromatic_intervals_in(expr):
   '''.. versionadded:: 1.1.2

   Return unordered set of chromatic intervals in `expr`. ::

      abjad> staff = Staff(construct.scale(4))
      abjad> pitchtools.get_chromatic_intervals_in(staff)
      abjad> for interval in pitchtools.get_chromatic_intervals_in(staff):
      ...     interval
      ... 
      ChromaticInterval(4)
      ChromaticInterval(2)
      ChromaticInterval(5)
      ChromaticInterval(2)
      ChromaticInterval(3)
      ChromaticInterval(1)
   '''
   
   chromatic_intervals = set([ ])
   pitches = get_pitches(expr)
   unordered_pitch_pairs = listtools.get_unordered_pairs(pitches)
   for unordered_pitch_pair in unordered_pitch_pairs:
      first_pitch = unordered_pitch_pair.pop( )
      second_pitch = unordered_pitch_pair.pop( )
      chromatic_interval_number = abs(first_pitch.number - second_pitch.number)
      chromatic_interval = ChromaticInterval(chromatic_interval_number)
      chromatic_intervals.add(chromatic_interval)      
   
   return chromatic_intervals
