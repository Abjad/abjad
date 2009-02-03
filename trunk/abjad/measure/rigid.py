from abjad.measure.base import _Measure
from abjad.meter.meter import Meter


class RigidMeasure(_Measure):

   def __init__(self, meter, music = None):
      _Measure.__init__(self, music)
      self.meter = meter

   ## NOTE: There's very little going on in this class because
   ##       _MeasureFormatter enforces the MisfilledMeasure
   ##       requirement, meaning that RigidMeasure doesn't
   ##       have to.
