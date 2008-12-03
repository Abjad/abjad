from abjad.containers.container import Container
from abjad.helpers.hasname import hasname
from abjad.helpers.in_terms_of import _in_terms_of
from abjad.measure.duration import _MeasureDurationInterface
from abjad.measure.formatter import _MeasureFormatter
from abjad.meter.meter import _Meter
from abjad.rational.rational import Rational
from math import log


class Measure(Container):

   def __init__(self, meter = None, music = None):
      music = music or [ ]
      Container.__init__(self, music)
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
   
   ### BOUND METHODS ###

   def trim(self, start, stop = 'unused'):
      old_denominator = self.meter.denominator
      if stop != 'unused':
         assert not (start == 0 and (stop is None or stop >= len(self)))
      if stop == 'unused':
         del(self[start])
      else:
         del(self[start : stop])
      naive_meter = self.duration.contents
      better_meter = _in_terms_of(naive_meter, old_denominator)
      self.meter = better_meter
