from abjad.container.container import Container
#from abjad.helpers.hasname import hasname
#from abjad.helpers.in_terms_of import _in_terms_of
from abjad.measure.duration import _MeasureDurationInterface
from abjad.measure.formatter import _MeasureFormatter
#from abjad.meter.meter import Meter
#from abjad.rational.rational import Rational
#from math import log


class _Measure(Container):

   def __init__(self, music = None):
      music = music or [ ]
      Container.__init__(self, music)
      self._duration = _MeasureDurationInterface(self)
      self.formatter = _MeasureFormatter(self)

   ### OVERLOADS ###

   def __repr__(self):
#      if getattr(self, 'meter', None) and len(self) > 0:
#         return 'Measure(%s, [%s])' % (self.meter, self._summary)
#      elif getattr(self, 'meter', None):
#         return 'Measure(%s)' % self.meter
#      elif len(self) > 0:
#         return 'Measure([%s])' % self._summary
#      else:
#         return 'Measure( )'
      class_name = self.__class__.__name__
      forced_meter = self.meter.forced
      summary = self._summary
      length = len(self)
      if forced_meter and length:
         return '%s(%s, [%s])' % (class_name, forced_meter, summary)
      elif forced_meter:
         return '%s(%s)' % (class_name, forced_meter)
      elif length:
         return '%s([%s])' % (class_name, summary)
      else:
         return '%s( )' % class_name

   def __str__(self):
#      if self.meter and len(self) > 0:
#         return '|%s, %s|' % (self.meter, self._summary)
#      elif self.meter:
#         return '|%s|' % self.meter
#      elif len(self) > 0:
#         return '|%s|' % self._summary
#      else:
#         return '| |'
      forced_meter = self.meter.forced
      summary = self._summary
      length = len(self)
      if forced_meter and length:
         return '|%s, %s|' % (forced_meter, summary)
      elif forced_meter:
         return '|%s|' % forced_meter
      elif length:
         return '|%s|' % summary
      else:
         return '| |'

   ### PUBLIC ATTRIBUTES ###

   @property
   def duration(self):
      return self._duration

#   @apply
#   def meter( ):
#      def fget(self):
#         return self._meter
#      def fset(self, arg):
#         if arg is None:
#            self._meter = None
#         else:
#            #meter = _Meter(*arg)
#            meter = Meter(arg)
#            self._meter = meter
#      return property(**locals( ))
   
#   ### PUBLIC METHODS ###
#
#   def trim(self, start, stop = 'unused'):
#      old_denominator = self.meter.denominator
#      if stop != 'unused':
#         assert not (start == 0 and (stop is None or stop >= len(self)))
#      if stop == 'unused':
#         del(self[start])
#      else:
#         del(self[start : stop])
#      naive_meter = self.duration.contents
#      better_meter = _in_terms_of(naive_meter, old_denominator)
#      self.meter = better_meter
