from abjad.tools.interpolate.divide import divide


def divide_multiple(totals, key_values, exp='cosine'):
   '''.. versionadded:: 1.1.2

   Interpolates between `key_values` such that the sum of the 
   resulting interpolated values equals the given `totals`.
   The operation is the same as ``interpolate.divide( )``, but this function
   takes multiple `totals` and `key_values` at once.

   Precondition: ``len(totals) == len(key_values) - 1``.

   - `totals` is a list or tuple of the total sum of interpolated values.
   - `key_values` is a list or tuple of key values to interpolate between.
   - `exp` in the interpolation exponent. If `exp` is 'cosine', the 
      interpolation is cosine, if numeric, then exponential.
   
   The function returns a list of floats.

   Example::

     abjad> interpolate.divide_multiple([100, 50], [20, 10, 20])
     [19.4487, 18.5201, 16.2270, 13.7156, 11.7488, 10.4879, 
     9.8515, 9.5130, 10.4213, 13.0736, 16.9918]

   .. todo:: fix hyphen chains in API entry so Sphinx doesn't complain.
   '''

   ## TODO: Here is the problematic example from the API entry.
   #   .     .    .   .  . ... .  .   .    .     .    .    .   .  . ...
   #   |--------------------|-------------------|---------------------|
   #         total[0]               total[1]            total[2] 
   #key_values[0]      key_values[1]       key_values[2]         key_values[3]

   assert len(totals) == len(key_values) - 1

   result = [ ]
   for i in range(len(totals)):
      dts = divide(totals[i], key_values[i], key_values[i+1], exp)
      ## we want a flat list
      result.extend(dts)
   return result

