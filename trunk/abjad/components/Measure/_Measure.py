from abjad.components.Container import Container
from abjad.components.Measure._MeasureDurationInterface import _MeasureDurationInterface
from abjad.components.Measure._MeasureFormatter import _MeasureFormatter
from abjad.tools import marktools


class _Measure(Container):
   '''Abstract base class of Abjad model of one measure in score.
   '''

   def __init__(self, music = None):
      Container.__init__(self, music)
      self._duration = _MeasureDurationInterface(self)
      self._explicit_meter = None
      self._formatter = _MeasureFormatter(self)

   ## OVERLOADS ##

   def __add__(self, arg):
      '''Add two measures together in-score or outside-of-score.
         Wrapper around measuretools.fuse_measures.'''
      assert isinstance(arg, _Measure)
      from abjad.tools import measuretools
      new = measuretools.fuse_measures([self, arg])
      return new

   def __repr__(self):
      '''String form of measure with parentheses for interpreter display.'''
      class_name = self.__class__.__name__
      forced_meter = self._explicit_meter
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
      forced_meter = marktools.get_effective_time_signature(self)
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

   ## PRIVATE METHODS ##

   #def _attach_explicit_meter(self, numerator, denominator, partial = None):
   def _attach_explicit_meter(self, *args, **kwargs):
      #print 'attaching explicit meter ...'
      from abjad.tools import marktools
      from abjad.tools import metertools
      if len(args) == 1 and isinstance(args[0], marktools.TimeSignatureMark):
         new_explicit_meter = args[0]
      elif len(args) == 1 and isinstance(args[0], metertools.Meter):
         numerator, denominator = args[0].numerator, args[0].denominator
         new_explicit_meter = marktools.TimeSignatureMark(numerator, denominator)
      elif len(args) == 2:
         numerator, denominator = args
         new_explicit_meter = marktools.TimeSignatureMark(numerator, denominator)
      else:
         raise ValueError('args "%s" not understood.' % str(args))
      partial = kwargs.get('partial', None)
      if partial is not None:
         raise Exception('implement partial meter.')
      if self._explicit_meter is not None:
         #print 'detaching old explicit meter ...'
         self._explicit_meter.detach_mark( )
      new_explicit_meter(self)
      self._explicit_meter = new_explicit_meter
      self._mark_entire_score_tree_for_later_update('marks')

   ## PRIVATE ATTRIBUTES ##

   @property
   def _compact_representation(self):
      '''Display form of measure used for spanners to display
      potentially many spanned measures one after the other.'''
      return '|%s(%s)|' % (marktools.get_effective_time_signature(self), len(self))

   ## PUBLIC ATTRIBUTES ##

   @property
   def full(self):
      '''True if preprolated duration matches effective meter duration.'''
      return marktools.get_effective_time_signature(self).duration == self.duration.preprolated

## FIXME ##
#   @property
#   def number(self):
#      '''Read-only measure number STARTING AT ONE, not zero.'''
#      #self._numbering._update_all_observer_interfaces_in_score_if_necessary( )
#      self._numbering._update_prolated_offset_values_of_all_score_components_if_necessary( )
#      self._numbering._update_observer_interfaces_of_all_score_components_if_necessary( )
#      return self._numbering._measure
