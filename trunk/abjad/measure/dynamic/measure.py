from abjad.measure.base import _Measure
from abjad.measure.dynamic.duration import _DynamicMeasureDurationInterface
from abjad.meter.meter import Meter
import types


class DynamicMeasure(_Measure):

   def __init__(self, music = None):
      _Measure.__init__(self, music)
      self._denominator = None
      self._duration = _DynamicMeasureDurationInterface(self)

   ### PUBLIC ATTRIBUTES ###

   @apply
   def denominator( ):
      def fget(self):
         return self._denominator
      def fset(self, arg):
         assert isinstance(arg, (int, long, types.NoneType))
         self._denominator = arg
      return property(**locals( ))

   @apply
   def meter( ):
      def fget(self):
         return self._meter
      return property(**locals( ))
