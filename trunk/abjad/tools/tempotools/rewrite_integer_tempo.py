import fractions
import math
from abjad.tools import durationtools
from abjad.tools import mathtools


def rewrite_integer_tempo(integer_tempo, maximum_numerator=None, maximum_denominator=None):
    r'''.. versionadded:: 2.0

    Rewrite `integer_tempo`.

    Allow no tempo less than half `integer_tempo` or greater than double `integer_tempo`::

        >>> pairs = tempotools.rewrite_integer_tempo(
        ...     58, maximum_numerator=8, maximum_denominator=8)

    ::

        >>> for pair in pairs:
        ...     pair
        ...
        (Multiplier(1, 2), 29)
        (Multiplier(1, 1), 58)
        (Multiplier(3, 2), 87)
        (Multiplier(2, 1), 116)

    Return list.
    '''

    # find divisors
    divisors = mathtools.divisors(integer_tempo)
    if maximum_denominator is not None:
      divisors = [x for x in divisors if x <= maximum_denominator]

    # make pairs
    pairs = []
    for divisor in divisors:
      start = int(math.ceil(divisor / 2.0))
      stop = 2 * divisor
      numerators = range(start, stop + 1)
      if maximum_numerator is not None:
            numerators = [x for x in numerators if x <= maximum_numerator]
      for numerator in numerators:
            multiplier = durationtools.Multiplier(numerator, divisor)
            new_tempo = fractions.Fraction(multiplier * integer_tempo)
            assert mathtools.is_integer_equivalent_number(new_tempo)
            new_tempo = int(new_tempo)
            pair = (multiplier, new_tempo)
            if pair not in pairs:
                pairs.append(pair)

    # sort pairs
    pairs.sort()

    # return pairs
    return pairs
