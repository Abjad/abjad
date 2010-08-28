from abjad.components.Measure._Measure import _Measure
from abjad.tools import durtools
from abjad.tools import marktools
from abjad.tools.measuretools.DynamicMeasure._DynamicMeasureDurationInterface import \
   _DynamicMeasureDurationInterface
from abjad.tools.measuretools.DynamicMeasure._DynamicMeasureMeterInterface import \
   _DynamicMeasureMeterInterface
from abjad.tools.metertools import Meter


class DynamicMeasure(_Measure):

   def __init__(self, music = None, **kwargs):
      _Measure.__init__(self, music)
      self._denominator = None
      self._duration = _DynamicMeasureDurationInterface(self)
      self._explicit_meter_is_current = False
      #self._meter = _DynamicMeasureMeterInterface(self, self._update)
      self._meter = _DynamicMeasureMeterInterface(self)
      self._initialize_keyword_values(**kwargs)
      self.suppress_meter = False

   ## PRIVATE METHODS ##

   def _update_explicit_meter(self):
      #print 'foo'
      if self.denominator:
         meter_pair = durtools.rational_to_duration_pair_with_specified_integer_denominator(
            self.duration.contents, self.denominator)
      else:
         meter_pair = (self.duration.contents.numerator, self.duration.contents.denominator)
      meter = marktools.TimeSignatureMark(*meter_pair, suppress = self.suppress_meter)
      self._attach_explicit_meter(meter)
      self._explicit_meter_is_current = True
      #print 'bar'

   ## PUBLIC ATTRIBUTES ##

   @apply
   def denominator( ):
      def fget(self):
         return self._denominator
      def fset(self, arg):
         assert isinstance(arg, (int, long, type(None)))
         self._denominator = arg
      return property(**locals( ))
