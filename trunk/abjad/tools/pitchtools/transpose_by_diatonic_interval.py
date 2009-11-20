def transpose_by_diatonic_interval(expr, diatonic_interval):
   '''.. versionadded:: 1.1.2

   Transpose all pitch carriers in `expr` by `diatonic_interval`. ::

      abjad>

   .. todo:: FINISH IMPLEMENTATION.
   '''

   if not isinstance(diatonic_interval, DiatonicInterval):
      raise TypeError('must be diatonic interval.')

   

def _transpose_pitch_carrier_by_diatonic_interval(
   pitch_carrier, diatonic_interval):

   if isinstance(pitch_carrier, Pitch):
      pitch_number = pitch_carrier.number
      pitch_number += diatonic_interval.semitones
      
