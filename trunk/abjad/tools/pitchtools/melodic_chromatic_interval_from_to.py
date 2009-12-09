from abjad.tools import mathtools
from abjad.tools.pitchtools.MelodicChromaticInterval import \
   MelodicChromaticInterval
from abjad.tools.pitchtools.get_pitch import get_pitch


def melodic_chromatic_interval_from_to(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return melodic chromatic interval from `pitch_carrier_1` to
   `pitch_carrier_2`. ::

      abjad> pitchtools.melodic_chromatic_interval_from_to(Pitch(-2), Pitch(12))
      MelodicChromaticInterval(+14)

   ::

      abjad> pitchtools.melodic_chromatic_interval_from_to(Pitch(12), Pitch(-2))
      MelodicChromaticInterval(-14)
   '''

   ## get pitches
   pitch_1 = get_pitch(pitch_carrier_1)
   pitch_2 = get_pitch(pitch_carrier_2)

   ## get difference in semitones
   number = pitch_2.number - pitch_1.number

   ## change 1.0, 2.0, ... into 1, 2, ...
   number = mathtools.trivial_float_to_int(number)   

   ## make melodic chromatic interval
   mci = MelodicChromaticInterval(number)

   ## return melodic chromatic interval
   return mci
