from abjad.tools.metertools.Meter import Meter
from fractions import Fraction
from abjad.tools import durtools


def is_meter_token(meter_token):
   '''True when `meter_token` has the form of an
   Abjad meter token. ::
   
      abjad> metertools.is_meter_token(metertools.Meter(3, 8))
      True

   ::

      abjad> metertools.is_meter_token(Fraction(3, 8))
      True

   ::

      abjad> metertools.is_meter_token((3, 8))        
      True

   Otherwise false. ::

      abjad> metertools.is_meter_token('text')
      False
   '''

   if isinstance(meter_token, Meter):
      return True
   elif isinstance(meter_token, Fraction):
      return True
   elif durtools.is_duration_pair(meter_token):
      return True
   else:
      return False
