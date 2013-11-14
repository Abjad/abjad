# -*- encoding: utf-8 -*-
import fractions
import math
from abjad.tools import durationtools
from abjad.tools import mathtools


def rewrite_integer_tempo(
    integer_tempo, 
    maximum_numerator=None, 
    maximum_denominator=None,
    ):
    r'''Rewrites `integer_tempo`.

    Returns new tempo indictions not less than half of `integer_tempo`
    and not more than twice `integer_tempo`.

    ..  container:: example

        Rewrites tempo ``58`` MM by ratios of the form ``n:d`` such that 
        ``1 <= n <= 8`` and ``1 <= d <= 8``:
        ...

        ::

            >>> pairs = tempotools.rewrite_integer_tempo(
            ...     58, 
            ...     maximum_numerator=8, 
            ...     maximum_denominator=8,
            ...     )

        ::

            >>> for tempo, ratio in pairs:
            ...     string = '{}\t{}'.format(tempo, ratio)
            ...     print string
            ...
            29  1:2
            58  1:1
            87  3:2
            116 2:1

    ..  container:: example

        Rewrites tempo ``58`` MM by ratios of the form ``n:d`` such that
        ``1 <= n <= 30`` and ``1 <= d <= 30``:

        ::

            >>> pairs = tempotools.rewrite_integer_tempo(
            ...     58, 
            ...     maximum_numerator=30, 
            ...     maximum_denominator=30,
            ...     )

        ::

            >>> for tempo, ratio in pairs:
            ...     string = '{}\t{}'.format(tempo, ratio)
            ...     print string
            ...
            29  1:2
            30  15:29
            32  16:29
            34  17:29
            36  18:29
            38  19:29
            40  20:29
            42  21:29
            44  22:29
            46  23:29
            48  24:29
            50  25:29
            52  26:29
            54  27:29
            56  28:29
            58  1:1
            60  30:29
            87  3:2
            116 2:1

    Returns list.
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
            ratio = mathtools.Ratio(numerator, divisor)
            multiplier = durationtools.Multiplier(*ratio)
            new_tempo = fractions.Fraction(multiplier * integer_tempo)
            assert mathtools.is_integer_equivalent_number(new_tempo)
            new_tempo = int(new_tempo)
            #pair = (ratio, new_tempo)
            pair = (new_tempo, ratio)
            if pair not in pairs:
                pairs.append(pair)

    # sort pairs
    pairs.sort()

    # return pairs
    return pairs
