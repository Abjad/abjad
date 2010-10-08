from abjad.tools import listtools


def pentatonic_pitch_number_to_chromatic_pitch_number(pentatonic_scale_degree, transpose=1, phase=0):
   '''Return integer chromatic pitch number corresponding to 
   integer `pentatonic_scale_degree`. ::

      abjad> for pentatonic_scale_degree in range(9):
      ...     chromatic_pitch_number = pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(pentatonic_scale_degree)
      ...     print '%s\\t%s' % (pentatonic_scale_degree, chromatic_pitch_number)
      ... 
      0  1
      1  3
      2  6
      3  8
      4  10
      5  13
      6  15
      7  18
      8  20

   Pentatonic scale degrees may be negative. ::

      abjad> for pentatonic_scale_degree in range(-1, -9, -1):
      ...     chromatic_pitch_number = pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number(pentatonic_scale_degree)
      ...     print '%s\\t%s' % (pentatonic_scale_degree, chromatic_pitch_number)
      ... 
      -1 -2
      -2 -4
      -3 -6
      -4 -9
      -5 -11
      -6 -14
      -7 -16
      -8 -18

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pentatonic_to_chromatic( )`` to
      ``pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.zero_indexed_pentatonic_scale_degree_number_to_pitch_number( )`` to
      ``pitchtools.pentatonic_pitch_number_to_chromatic_pitch_number( )``.
   '''

   assert isinstance(pentatonic_scale_degree, int)
   assert isinstance(phase, int)
   assert 0 <= phase
   assert phase < 5

   penta_intervals = [2,3,2,2,3] * 2
   penta = dict(zip([0,1,2,3,4],
      listtools.cumulative_sums_zero(penta_intervals[phase:phase+5])))
   pclass = pentatonic_scale_degree % 5
   octave = pentatonic_scale_degree // 5
   return 12 * octave + penta[pclass] + transpose
