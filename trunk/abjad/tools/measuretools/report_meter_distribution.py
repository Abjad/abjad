from abjad.measure.measure import _Measure
from abjad.tools import iterate
import itertools


## TODO: Write measuretools.report_meter_distribution( ) tests. ##

def report_meter_distribution(expr, delivery = 'screen'):
   '''Inventory meters in 'expr' with frequency count of each.
   
      >>> measuretools.report_meter_distribution(t)
        2/16    62
        3/16    14
        4/16    66
        5/16    57
        6/16    17
        7/16    20
        8/16    16
        9/16    19
        10/16   4'''

   meters = [ ]
   for measure in iterate.naive(expr, _Measure):
      meters.append(measure.meter.effective)
      
   meters.sort( )

   result = ''
   for key, values_generator in itertools.groupby(meters):
      result += '\t%s\t%s\n' % (key, len(list(values_generator)))

   if delivery == 'screen':
      print result
   elif delivery == 'string':
      return result
   else:
      raise ValueError("delivery must be 'screen' or 'string'.")
