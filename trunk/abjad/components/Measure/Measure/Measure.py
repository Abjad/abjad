from abjad.components.Measure._Measure import _Measure
#from abjad.components.Measure.Measure._RigidMeasureFormatter import _RigidMeasureFormatter
from abjad.tools.metertools import Meter
from abjad.tools import durtools
from abjad.tools import marktools


class Measure(_Measure):

   def __init__(self, meter, music = None, **kwargs):
      _Measure.__init__(self, music)
      #self._formatter = _RigidMeasureFormatter(self)
      meter = Meter(meter)
      numerator, denominator = meter.numerator, meter.denominator
      self._attach_explicit_meter(numerator, denominator)
      self._initialize_keyword_values(**kwargs)

   ## OVERLOADS ##

   def __delitem__(self, i):
      '''Container deletion with meter adjustment.'''
      try:
         old_denominator = marktools.get_effective_time_signature(self).denominator
      except AttributeError:
         pass
      _Measure.__delitem__(self, i)
      try:
         naive_meter = self.duration.preprolated
         better_meter = durtools.rational_to_duration_pair_with_specified_integer_denominator(
            naive_meter, old_denominator)
         self._attach_explicit_meter(*better_meter)
      except (AttributeError, UnboundLocalError):
         pass
