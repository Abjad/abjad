from abjad.container.container import Container
from abjad.measure.duration import _MeasureDurationInterface
from abjad.measure.formatter import _MeasureFormatter


class _Measure(Container):

   def __init__(self, music = None):
      music = music or [ ]
      Container.__init__(self, music)
      self._duration = _MeasureDurationInterface(self)
      self.formatter = _MeasureFormatter(self)

   ## OVERLOADS ##

   def __repr__(self):
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

   ## PUBLIC ATTRIBUTES ##

   @property
   def duration(self):
      return self._duration

   @property
   def full(self):
      return self.meter.effective.duration == self.duration.preprolated
