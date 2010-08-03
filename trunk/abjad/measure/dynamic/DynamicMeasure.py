from abjad.measure.measure import _Measure
from abjad.measure.dynamic.duration import _DynamicMeasureDurationInterface
from abjad.measure.dynamic.meter import _DynamicMeasureMeterInterface
from abjad.meter import Meter
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
