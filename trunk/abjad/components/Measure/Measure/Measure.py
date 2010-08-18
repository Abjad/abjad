from abjad.components.Measure._Measure import _Measure
from abjad.components.Measure.Measure._RigidMeasureDurationInterface import _RigidMeasureDurationInterface
from abjad.components.Measure.Measure._RigidMeasureFormatter import _RigidMeasureFormatter
from abjad.tools.metertools import Meter
from abjad.tools import durtools


class Measure(_Measure):

   def __init__(self, meter, music = None, **kwargs):
      _Measure.__init__(self, music)
      self._duration = _RigidMeasureDurationInterface(self)
      self._formatter = _RigidMeasureFormatter(self)
      self.meter.forced = Meter(meter)
      self._initialize_keyword_values(**kwargs)

   ## OVERLOADS ##

   def __delitem__(self, i):
      '''Container deletion with meter adjustment.'''
      try:
         old_denominator = self.meter.forced.denominator
      except AttributeError:
         pass
      _Measure.__delitem__(self, i)
      try:
         naive_meter = self.duration.preprolated
         better_meter = durtools.rational_to_duration_pair_with_specified_integer_denominator(naive_meter, old_denominator)
         self.meter.forced = Meter(better_meter)
      except (AttributeError, UnboundLocalError):
         pass
