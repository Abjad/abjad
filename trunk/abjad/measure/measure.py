from abjad.container import Container
from abjad.measure.duration import _MeasureDurationInterface
from abjad.measure.formatter import _MeasureFormatter


class _Measure(Container):
   '''Abstract base class of *Abjad* model of one measure in score.'''

   def __init__(self, music = None):
      '''Init measure as a type of *Abjad* container.
         Init dedicated duration interface and formatter.'''
      Container.__init__(self, music)
      self._duration = _MeasureDurationInterface(self)
      self._formatter = _MeasureFormatter(self)

   ## OVERLOADS ##

   def __add__(self, arg):
      '''Add two measures together in-score or outside-of-score.
         Wrapper around fuse.measures_by_reference.'''
      assert isinstance(arg, _Measure)
      from abjad.tools import fuse
      new = fuse.measures_by_reference([self, arg])
      return new

   def __repr__(self):
      '''String form of measure with parentheses for interpreter display.'''
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
      '''String form of measure with pipes for single string display.'''
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
   def full(self):
      '''True if preprolated duration matches effective meter duration.'''
      return self.meter.effective.duration == self.duration.preprolated

   @property
   def number(self):
      '''Read-only measure number STARTING AT ONE, not zero.'''
      self._numbering._makeSubjectUpdateIfNecessary( )
      return self._numbering._measure
