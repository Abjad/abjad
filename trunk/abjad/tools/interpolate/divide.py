from abjad.rational import Rational
from abjad.tools.interpolate.cosine import cosine
from abjad.tools.interpolate.exponential import exponential


def divide(total, start_frac, stop_frac, exp='cosine'):
   '''Divide `total` into segments of sizes computed from interpolating 
      between `start_frac` and `stop_frac`. 
      Set ``exp='cosine'`` for cosine interpolation. This is the default. 
      If set to a numeric value, the interpolation is exponential and 
      `exp` is the exponent.
      The resulting segments are scaled so that their sum equals `total`
      exactly.

      The function returns a list of floats.

      Examples::

         abjad> interpolate.divide(10, 1, 1, exp=1)
         [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
         abjad> sum(_)
         10.0

         abjad> interpolate.divide(10, 5, 1)
         [4.7986734489043181, 2.8792040693425909, 1.3263207210948171, 
         0.99580176065827419]
         abjad> sum(_)
         10.0 
   '''

   if total <=0 :
      raise ValueError("'total' must be > 0.")
   if start_frac <= 0 or stop_frac <= 0:
      raise ValueError("Both 'start_frac' and 'stop_frac' must be > 0.")
   if (stop_frac + start_frac) > total:
      raise ValueError("'start_frac' + 'stop_frac' must be < 'total'.")

   result = [ ]
   total = float(total)
   partial_sum = 0
   while partial_sum < total:
      if exp == 'cosine':
         ip = cosine(start_frac, stop_frac, partial_sum / total)
      else:
         ip = exponential(start_frac, stop_frac, partial_sum / total, exp)
      result.append(ip)
      partial_sum += ip

   ## scale result to fit total exaclty
   result = [x * total / sum(result) for x in result]
   #result = [Rational(int(round(x * 10000, 5)), 10000) for x in result]
   return result

