from abjad.measure.measure import _Measure
from abjad.measure.rigid.duration import _RigidMeasureDurationInterface
from abjad.measure.rigid.formatter import _RigidMeasureFormatter


class RigidMeasure(_Measure):

   def __init__(self, meter, music = None):
      _Measure.__init__(self, music)
      self._duration = _RigidMeasureDurationInterface(self)
      self._formatter = _RigidMeasureFormatter(self)
      self.meter = meter
