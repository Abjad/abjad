from abjad.components._Measure._Measure import _Measure
from abjad.components._Measure.RigidMeasure._RigidMeasureDurationInterface import \
   _RigidMeasureDurationInterface
from abjad.components._Measure.RigidMeasure._RigidMeasureFormatter import _RigidMeasureFormatter
from abjad.marks import Meter
from abjad.tools import durtools


class RigidMeasure(_Measure):

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
