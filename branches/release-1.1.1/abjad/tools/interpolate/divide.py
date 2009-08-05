from abjad.rational import Rational
from abjad.tools.interpolate.cosine import cosine
from abjad.tools.interpolate.exponential import exponential


def divide(total, start_frac, stop_frac, exp='cosine'):
   '''Divide total into segments of sizes computed from interpolating 
      between start_frac and stop_frac. 
      Set exp='cosine' for cosine interpolation. This is the default. If set
      to a numeric value, the interpolation is exponential and exp is the 
      exponent.'''

   if stop_frac >= total or start_frac >= total:
      raise ValueError('Both dividing fractions must be smaller than total.')

   result = [ ]
   total = float(total)
   while sum(result) < total:
      if exp == 'cosine':
         ip = cosine(start_frac, stop_frac, sum(result) / total)
      else:
         ip = exponential(start_frac, stop_frac, sum(result) / total, exp)
      result.append(ip)
   result = [x * total / sum(result) for x in result]
   result = [Rational(int(round(x * 10000, 5)), 10000) for x in result]
   return result

#   while sum(result) <= (total - stop_frac):
#      if exp == 'cosine':
#         ip = cosine(start_frac, stop_frac, sum(result) / total)
#      else:
#         ip = exponential(start_frac, stop_frac, sum(result) / total, exp)
#      ip = int(round(ip * 10000, 5))
#      ip = Rational(ip, 10000)
#      result.append(ip)
#   result[-1] += total - sum(result)
#   return result

