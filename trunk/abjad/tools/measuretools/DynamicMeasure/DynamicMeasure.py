from abjad.components.Measure.Measure import Measure
from abjad.tools import durtools
from abjad.tools import contexttools
from abjad.tools.measuretools.DynamicMeasure._DynamicMeasureDurationInterface import \
   _DynamicMeasureDurationInterface


class DynamicMeasure(Measure):

   __slots__ = ('_denominator', '_explicit_meter_is_current', 'suppress_meter', )

   def __init__(self, music = None, **kwargs):
      #_Measure.__init__(self, music)
      Measure.__init__(self, meter = (99, 99), music = music, **kwargs)
      self._denominator = None
      self._duration = _DynamicMeasureDurationInterface(self)
      self._explicit_meter_is_current = False
      #self._initialize_keyword_values(**kwargs)
      self.suppress_meter = False
      self._update_explicit_meter( )

   ## PRIVATE METHODS ##

   def _update_explicit_meter(self):
      if self.denominator:
         meter_pair = durtools.rational_to_duration_pair_with_specified_integer_denominator(
            self.duration.contents, self.denominator)
      else:
         meter_pair = (self.duration.contents.numerator, self.duration.contents.denominator)
      meter = contexttools.TimeSignatureMark(*meter_pair, suppress = self.suppress_meter)
      self._attach_explicit_meter(meter)
      self._explicit_meter_is_current = True

   ## PUBLIC ATTRIBUTES ##

   @apply
   def denominator( ):
      def fget(self):
         return self._denominator
      def fset(self, arg):
         assert isinstance(arg, (int, long, type(None)))
         self._denominator = arg
         self._update_explicit_meter( )
      return property(**locals( ))

   ## PUBLIC METHODS ##

   def extend(self, expr):
      Measure.extend(self, expr)
      self._update_explicit_meter( )
