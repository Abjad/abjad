from abjad.tools import mathtools
from abjad.tools.pitchtools.MelodicChromaticInterval import MelodicChromaticInterval
from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import \
   get_named_chromatic_pitch_from_pitch_carrier


def calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return melodic chromatic interval from `pitch_carrier_1` to
   `pitch_carrier_2`. ::

      abjad> pitchtools.calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(NamedPitch(-2), NamedPitch(12))
      MelodicChromaticInterval(+14)

   ::

      abjad> pitchtools.calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(NamedPitch(12), NamedPitch(-2))
      MelodicChromaticInterval(-14)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.melodic_chromatic_interval_from_to( )`` to
      ``pitchtools.calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.calculate_melodic_chromatic_interval_from_pitch_to_pitch( )`` to
      ``pitchtools.calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier( )``.
   '''

   ## get pitches
   pitch_1 = get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_1)
   pitch_2 = get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_2)

   ## get difference in semitones
   number = pitch_2.pitch_number - pitch_1.pitch_number

   ## change 1.0, 2.0, ... into 1, 2, ...
   number = mathtools.trivial_float_to_int(number)   

   ## make melodic chromatic interval
   mci = MelodicChromaticInterval(number)

   ## return melodic chromatic interval
   return mci
