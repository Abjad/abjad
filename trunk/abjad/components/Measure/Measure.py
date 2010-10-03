from abjad.components.Container import Container
from abjad.components.Measure._MeasureDurationInterface import _MeasureDurationInterface
from abjad.components.Measure._MeasureFormatter import _MeasureFormatter
from abjad.tools import durtools
from abjad.tools import contexttools
from abjad.tools.metertools import Meter


class Measure(Container):
   r'''The Abjad model of a measure:

   ::

      abjad> measure = Measure((4, 8), macros.scale(4))
      abjad> f(measure)
      {
         \time 4/8
         c'8
         d'8
         e'8
         f'8
      }
   '''

   def __init__(self, meter, music = None, **kwargs):
      Container.__init__(self, music)
      self._duration = _MeasureDurationInterface(self)
      self._explicit_meter = None
      self._formatter = _MeasureFormatter(self)

      meter = Meter(meter)
      numerator, denominator = meter.numerator, meter.denominator
      self._attach_explicit_meter(numerator, denominator)

      self._initialize_keyword_values(**kwargs)


   ## OVERLOADS ##

   def __add__(self, arg):
      '''Add two measures together in-score or outside-of-score.
      Wrapper around measuretools.fuse_measures.
      '''
      assert isinstance(arg, type(self))
      from abjad.tools import measuretools
      new = measuretools.fuse_measures([self, arg])
      return new

   def __delitem__(self, i):
      '''Container deletion with meter adjustment.'''
      try:
         old_denominator = contexttools.get_effective_time_signature(self).denominator
      except AttributeError:
         pass
      #_Measure.__delitem__(self, i)
      Container.__delitem__(self, i)
      try:
         naive_meter = self.duration.preprolated
         better_meter = durtools.rational_to_duration_pair_with_specified_integer_denominator(
            naive_meter, old_denominator)
         self._attach_explicit_meter(*better_meter)
      except (AttributeError, UnboundLocalError):
         pass

   def __repr__(self):
      '''String form of measure with parentheses for interpreter display.
      '''
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
      '''String form of measure with pipes for single string display.
      '''
      forced_meter = contexttools.get_effective_time_signature(self)
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

   def _attach_explicit_meter(self, *args, **kwargs):
      #print 'attaching explicit meter ...'
      from abjad.tools import contexttools
      from abjad.tools import metertools
      if len(args) == 1 and isinstance(args[0], contexttools.TimeSignatureMark):
         new_explicit_meter = args[0]
      elif len(args) == 1 and isinstance(args[0], metertools.Meter):
         numerator, denominator = args[0].numerator, args[0].denominator
         new_explicit_meter = contexttools.TimeSignatureMark(numerator, denominator)
      elif len(args) == 2:
         numerator, denominator = args
         new_explicit_meter = contexttools.TimeSignatureMark(numerator, denominator)
      else:
         raise ValueError('args not understood: "%s".' % str(args))
      partial = kwargs.get('partial', None)
      if partial is not None:
         raise NotImplementedError('partial meter not yet implemented.')
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
      potentially many spanned measures one after the other.
      '''
      return '|%s(%s)|' % (contexttools.get_effective_time_signature(self), len(self))

   ## PUBLIC ATTRIBUTES ##

   @property
   def is_full(self):
      '''True if preprolated duration matches effective meter duration.
      '''
      return contexttools.get_effective_time_signature(self).duration == self.duration.preprolated
