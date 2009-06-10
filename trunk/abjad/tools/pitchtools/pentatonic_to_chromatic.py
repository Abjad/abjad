from abjad.tools import mathtools


def pentatonic_to_chromatic(num, transpose=1, phase=0):
   '''Map pentatonic scale degree to chromatic scale degree.
      Default interfal configuration is the 'black keys on the piano'.
      Default interva sequence is 2,3,2,2,3
      Scale degrees are 0 based.
      0 --> 0
      1 --> 2
      2 --> 5
      3 --> 7
      4 --> 9'''

   assert isinstance(num, int)
   assert isinstance(phase, int)
   assert phase >= 0
   assert phase < 5

   penta_intervals = [2,3,2,2,3] * 2
   penta = dict(zip([0,1,2,3,4],
      mathtools.cumulative_sums_zero(penta_intervals[phase:phase+5])))
   pclass = num % 5
   octave = num // 5
   return 12 * octave + penta[pclass] + transpose
