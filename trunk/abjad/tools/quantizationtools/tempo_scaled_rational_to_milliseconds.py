from abjad import Fraction
from abjad.tools.contexttools import TempoMark


def tempo_scaled_rational_to_milliseconds(rational, tempo):

   assert isinstance(rational, (int, Fraction))
   assert isinstance(tempo, TempoMark)

   whole_note_duration = 1000 \
      * Fraction(tempo.duration.denominator, tempo.duration.numerator) \
      * Fraction(60, tempo.units_per_minute)

   return rational * whole_note_duration
