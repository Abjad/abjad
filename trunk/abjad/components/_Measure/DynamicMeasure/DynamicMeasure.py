from abjad.components._Measure._Measure import _Measure
from abjad.components._Measure.DynamicMeasure._DynamicMeasureDurationInterface import \
   _DynamicMeasureDurationInterface
from abjad.components._Measure.DynamicMeasure._DynamicMeasureMeterInterface import \
   _DynamicMeasureMeterInterface
from abjad.marks import Meter
import types


class DynamicMeasure(_Measure):

   def __init__(self, music = None, **kwargs):
      _Measure.__init__(self, music)
      self._denominator = None
      self._duration = _DynamicMeasureDurationInterface(self)
      self._meter = _DynamicMeasureMeterInterface(self, self._update)
      self._initialize_keyword_values(**kwargs)

   ## PUBLIC ATTRIBUTES ##

   @apply
   def denominator( ):
      def fget(self):
         return self._denominator
      def fset(self, arg):
         assert isinstance(arg, (int, long, type(None)))
         self._denominator = arg
      return property(**locals( ))
