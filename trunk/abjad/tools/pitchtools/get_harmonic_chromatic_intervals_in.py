from abjad.tools import listtools
from abjad.tools.pitchtools.HarmonicChromaticInterval import \
   HarmonicChromaticInterval
from abjad.tools.pitchtools.get_pitches import get_pitches


def get_harmonic_chromatic_intervals_in(expr):
   '''.. versionadded:: 1.1.2

   Return unordered set of harmonic chromatic intervals in `expr`. ::

      abjad> staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> pitchtools.get_harmonic_chromatic_intervals_in(staff)
      abjad> for interval in pitchtools.get_harmonic_chromatic_intervals_in(staff):
      ...     interval
      ... 
      HarmonicChromaticInterval(4)
      HarmonicChromaticInterval(2)
      HarmonicChromaticInterval(5)
      HarmonicChromaticInterval(2)
      HarmonicChromaticInterval(3)
      HarmonicChromaticInterval(1)
   '''
   
   chromatic_intervals = [ ]
   pitches = get_pitches(expr)
   unordered_pitch_pairs = listtools.get_unordered_pairs(pitches)
   for first_pitch, second_pitch in unordered_pitch_pairs:
      chromatic_interval_number = abs(first_pitch.number - second_pitch.number)
      chromatic_interval = HarmonicChromaticInterval(chromatic_interval_number)
      chromatic_intervals.append(chromatic_interval)      
   
   return chromatic_intervals
