from abjad.tools import listtools


def zero_indexed_diatonic_scale_degree_number_to_pitch_number(diatonic_scale_degree, transpose=0, phase=0):
   '''Return integer chromatic pitch number corresponding to integer
   `diatonic_scale_degree`.

   Defaults to the white keys on the piano in Ionian mode. ::

      abjad> for diatonic_scale_degree in range(9):
      ...     chromatic_pitch_number = pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(diatonic_scale_degree)
      ...     print '%s\\t%s' % (diatonic_scale_degree, chromatic_pitch_number)
      ... 
      0  0
      1  2
      2  4
      3  5
      4  7
      5  9
      6  11
      7  12
      8  14

   Diatonic scale degrees may be negative. ::

      abjad> for diatonic_scale_degree in range(-1, -9, -1):
      ...     chromatic_pitch_number = pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(diatonic_scale_degree)
      ...     print '%s\\t%s' % (diatonic_scale_degree, chromatic_pitch_number)
      ... 
      -1 -1
      -2 -3
      -3 -5
      -4 -7
      -5 -8
      -6 -10
      -7 -12
      -8 -13

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.diatonic_to_chromatic( )`` to
      ``pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number( )``.
   '''

   assert isinstance(diatonic_scale_degree, int)
   assert isinstance(phase, int)
   assert 0 <= phase
   assert phase < 7

   dia_intervals = [2,2,1,2,2,2,1] * 2
   diatonic = dict(zip([0,1,2,3,4,5,6], 
      listtools.cumulative_sums_zero(dia_intervals[phase:phase+7])))
   pclass = diatonic_scale_degree % 7
   octave = diatonic_scale_degree // 7
   return 12 * octave + diatonic[pclass] + transpose
