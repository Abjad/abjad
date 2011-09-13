from abjad.tools import mathtools
from fractions import Fraction
import math


def integer_tempo_to_multiplier_tempo_pairs(integer_tempo,
    maximum_numerator = None, maximum_denominator = None):
    r'''.. versionadded:: 2.0

    Return all multiplier, tempo pairs possible from `integer_tempo`.

    Tempi must be no less than ``integer_tempo / 2`` and not greater
    than ``2 * integer_tempo``::

      abjad> from abjad.tools import tempotools

    ::

      abjad> pairs = tempotools.integer_tempo_to_multiplier_tempo_pairs(58, 8, 8)
      abjad> for pair in pairs:
      ...     pair
      ...
      (Fraction(1, 2), Fraction(29, 1))
      (Fraction(1, 1), Fraction(58, 1))
      (Fraction(3, 2), Fraction(87, 1))
      (Fraction(2, 1), Fraction(116, 1))

    Return list.
    '''

    pairs = []
    divisors = mathtools.divisors(integer_tempo)
    if maximum_denominator is not None:
      divisors = [x for x in divisors if x <= maximum_denominator]
    for divisor in divisors:
      start = int(math.ceil(divisor / 2.0))
      stop = 2 * divisor
      numerators = range(start, stop + 1)
      if maximum_numerator is not None:
            numerators = [x for x in numerators if x <= maximum_numerator]
      for numerator in numerators:
            multiplier = Fraction(numerator, divisor)
            new_tempo = multiplier * integer_tempo
            pair = (multiplier, new_tempo)
            if pair not in pairs:
                pairs.append(pair)
    pairs.sort()
    return pairs
