from abjad.duration.rational import Rational
from abjad.measure.duration import _MeasureDurationInterface
from .. containers.container import Container
#from .. containers.duration import _ContainerDurationInterface
from formatter import _MeasureFormatter
from .. helpers.hasname import hasname
from math import log
from meter import _Meter

class Measure(Container):

   def __init__(self, meter = None, music = [ ]):
      Container.__init__(self, music)
      #self._duration = _ContainerDurationInterface(self)
      self._duration = _MeasureDurationInterface(self)
      self.formatter = _MeasureFormatter(self)
      self.meter = meter

   ### REPR ###

   def __repr__(self):
      if self.meter and len(self) > 0:
         return 'Measure(%s, [%s])' % (self.meter, self._summary)
      elif self.meter:
         return 'Measure(%s)' % self.meter
      elif len(self) > 0:
         return 'Measure([%s])' % self._summary
      else:
         return 'Measure( )'

   def __str__(self):
      if self.meter and len(self) > 0:
         return '|%s, %s|' % (self.meter, self._summary)
      elif self.meter:
         return '|%s|' % self.meter
      elif len(self) > 0:
         return '|%s|' % self._summary
      else:
         return '| |'

   ### DERIVED PROPERTIES ###

   @property
   def nonbinary(self):
      if self.meter is not None:
         return bool(self.meter.denominator & (self.meter.denominator - 1))
      else:
         return False

   @property
   def _multiplier(self):
      if self.meter:
         d = self.meter.denominator
         return (2 ** int(log(d, 2)), d)
      else:
         return (1, 1)
  
   @property
   def duration(self):
      return self._duration

   ### MANAGED ATTRIBUTES ###

   @apply
   def meter( ):
      def fget(self):
         return self._meter
      def fset(self, arg):
         if arg is None:
            self._meter = None
         else:
            meter = _Meter(*arg)
            self._meter = meter
      return property(**locals( ))
