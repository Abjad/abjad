from abjad.tools import durtools
from abjad.tools.metertools.Meter import Meter
from fractions import Fraction


def is_meter_token(expr):
   '''True when `expr` has the form of an Abjad meter token::
   
      abjad> metertools.is_meter_token(metertools.Meter(3, 8))
      True

   ::

      abjad> metertools.is_meter_token(Fraction(3, 8))
      True

   ::

      abjad> metertools.is_meter_token((3, 8))        
      True

   Otherwise false::

      abjad> metertools.is_meter_token('text')
      False
   '''

   if isinstance(expr, Meter):
      return True
   elif isinstance(expr, Fraction):
      return True
   elif durtools.is_duration_pair(expr):
      return True
   else:
      return False
