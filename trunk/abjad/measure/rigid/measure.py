from abjad.measure.measure import _Measure
from abjad.measure.rigid.duration import _RigidMeasureDurationInterface
from abjad.measure.rigid.formatter import _RigidMeasureFormatter
from abjad.meter import Meter
from abjad.tools import durtools


class RigidMeasure(_Measure):

   def __init__(self, meter, music = None):
      _Measure.__init__(self, music)
      self._duration = _RigidMeasureDurationInterface(self)
      self._formatter = _RigidMeasureFormatter(self)
      self.meter.forced = Meter(meter)

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
         better_meter = durtools.rational_to_duration_pair_with_integer_denominator(naive_meter, old_denominator)
         self.meter.forced = Meter(better_meter)
      except (AttributeError, UnboundLocalError):
         pass
