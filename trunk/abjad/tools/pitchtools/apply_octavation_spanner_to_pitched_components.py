from abjad.tools.spannertools import OctavationSpanner
from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr


def apply_octavation_spanner_to_pitched_components(expr, 
   ottava_diatonic_pitch_number = None, quindecisima_diatonic_pitch_number = None):
   r""".. versionadded:: 1.1.1

   Apply octavation spanner to `expr` according to the diatonic pitch number
   of the maximum pitch in `expr`. ::

      abjad> t = Measure((4, 8), notetools.make_notes([24, 26, 27, 29], [(1, 8)]))
      abjad> pitchtools.apply_octavation_spanner_to_pitched_components(t, ottava_diatonic_pitch_number = 14)
      spannertools.OctavationSpanner(|4/8, c'''8, d'''8, ef'''8, f'''8|)

   ::

      abjad> print t.format
         \time 4/8
         \ottava #1
         c'''8
         d'''8
         ef'''8
         f'''8
         \ottava #0
   """

   pitches = list_named_chromatic_pitches_in_expr(expr)
   max_pitch = max(pitches)
   max_diatonic_pitch_number = max_pitch.diatonic_pitch_number

   if ottava_diatonic_pitch_number is not None:
      if ottava_diatonic_pitch_number <= max_diatonic_pitch_number:
         octavation = OctavationSpanner(expr)   
         octavation.start = 1
         if quindecisima_diatonic_pitch_number is not None:
            if quindecisima_diatonic_pitch_number <= max_diatonic_pitch_number:
               octavation.start = 2
         #else:
         #   octavation.start = 1

   try:
      return octavation
   except NameError:
      return None
