from abjad.tools import mathtools
from fractions import Fraction


denominators = range(4, 15 + 1) + range(16, 30 + 1, 2)
multipliers = set([ ])
for denominator in denominators:
    base_denominator = mathtools.greatest_power_of_two_less_equal(denominator)
    multiplier = Fraction(base_denominator, denominator)
    ratio = '%s:%s' % (multiplier.denominator, multiplier.numerator)
    #print ratio, '\t', multiplier * Fraction(1, base_denominator)
    multipliers.add(multiplier)

sargasso_multipliers = tuple(sorted(multipliers))
output_preamble_lines = ['from fractions import Fraction\n']
