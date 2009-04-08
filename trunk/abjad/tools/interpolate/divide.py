from abjad.rational.rational import Rational
from abjad.tools.interpolate.cosine import cosine
from abjad.tools.interpolate.exponential import exponential


def divide(total, start_frac, stop_frac, exp='cosine'):
   '''Divide total into segments of sizes computed from interpolating 
      between start_frac and stop_frac. 
      Set exp='cosine' for cosine interpolation. This is the default. If set
      to a numeric value, the interpolation is exponential and exp is the 
      exponent.'''

   result =  [ ]
   ip = 0
   cumulative = 0
   while cumulative <= total - stop_frac:
      if exp == 'cosine':
         ip = cosine(start_frac, stop_frac,
            cumulative / total)
      else:
         ip = exponential(start_frac, stop_frac,
            cumulative / total, exp)
      ip = int(round(ip * 10000, 5))
      ip = Rational(ip, 10000)
      result.append(ip)
      cumulative += ip
   residue = total - cumulative
   result[-1] += residue
   return result
