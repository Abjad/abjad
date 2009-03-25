from abjad.helpers.in_terms_of import _in_terms_of
from abjad.measure.base import _Measure
from abjad.measure.rigid.duration import _RigidMeasureDurationInterface
from abjad.measure.rigid.formatter import _RigidMeasureFormatter
from abjad.meter.meter import Meter


class RigidMeasure(_Measure):

   def __init__(self, meter, music = None):
      _Measure.__init__(self, music)
      self._duration = _RigidMeasureDurationInterface(self)
      self._formatter = _RigidMeasureFormatter(self)
      self.meter = meter

   ## PUBLIC METHODS ##

   def trim(self, start, stop = 'unused'):
      old_denominator = self.meter.forced.denominator
      if stop != 'unused':
         assert not (start == 0 and (stop is None or stop >= len(self)))
      if stop == 'unused':
         del(self[start])
      else:
         del(self[start : stop])
      naive_meter = self.duration.preprolated
      better_meter = _in_terms_of(naive_meter, old_denominator)
      self.meter = better_meter
