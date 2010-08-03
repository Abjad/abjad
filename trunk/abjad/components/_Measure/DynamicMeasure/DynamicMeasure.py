from abjad.components._Measure._Measure import _Measure
from abjad.components._Measure.DynamicMeasure.duration import _DynamicMeasureDurationInterface
from abjad.components._Measure.DynamicMeasure.meter import _DynamicMeasureMeterInterface
from abjad.Meter import Meter
import types


class DynamicMeasure(_Measure):

   def __init__(self, music = None):
      _Measure.__init__(self, music)
      self._denominator = None
      self._duration = _DynamicMeasureDurationInterface(self)
      self._meter = _DynamicMeasureMeterInterface(self, self._update)

   ## PUBLIC ATTRIBUTES ##

   @apply
   def denominator( ):
      def fget(self):
         return self._denominator
      def fset(self, arg):
         assert isinstance(arg, (int, long, types.NoneType))
         self._denominator = arg
      return property(**locals( ))
