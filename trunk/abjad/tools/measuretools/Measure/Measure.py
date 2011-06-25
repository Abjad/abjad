from abjad.tools import contexttools
from abjad.tools import durtools
from abjad.tools.containertools.Container import Container
from abjad.tools.measuretools.Measure._MeasureDurationInterface import _MeasureDurationInterface
from abjad.tools.measuretools.Measure._MeasureFormatter import _MeasureFormatter
import copy


class Measure(Container):
   r'''.. versionadded:: 1.1.1

   Abjad model of a measure::

      abjad> measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
   
   ::

      abjad> measure
      Measure(4/8, [c'8, d'8, e'8, f'8])

   ::

      abjad> f(measure)
      {
         \time 4/8
         c'8
         d'8
         e'8
         f'8
      }

   Return measure object.
   '''

   __slots__ = ( )

   def __init__(self, meter, music = None, **kwargs):
      Container.__init__(self, music)
      self._duration = _MeasureDurationInterface(self)
      self._formatter = _MeasureFormatter(self)
      meter = contexttools.TimeSignatureMark(meter)
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

   ## essentially the same as Container.__copy__.
   ## the definition given here adds one line to remove
   ## time signature immediately after instantiation
   ## because the mark-copying code will then provide time signature.
   def __copy__(self, *args):
      from abjad.tools import contexttools
      from abjad.tools import marktools
      from abjad.tools import markuptools
      new = type(self)(*self.__getnewargs__( ))
      ## only this line differs from Container.__copy__
      contexttools.detach_time_signature_mark_attached_to_component(new)
      if getattr(self, '_override', None) is not None:
         new._override = copy.copy(self.override)
      if getattr(self, '_set', None) is not None:
         new._set = copy.copy(self.set)
      for mark in marktools.get_marks_attached_to_component(self):
         new_mark = copy.copy(mark)
         new_mark.attach_mark(new)
      return new

   def __delitem__(self, i):
      '''Container deletion with meter adjustment.
      '''
      try:
         old_denominator = contexttools.get_effective_time_signature(self).denominator
      except AttributeError:
         pass
      Container.__delitem__(self, i)
      try:
         naive_meter = self.duration.preprolated
         better_meter = durtools.rational_to_duration_pair_with_specified_integer_denominator(
            naive_meter, old_denominator)
         self._attach_explicit_meter(*better_meter)
      except (AttributeError, UnboundLocalError):
         pass

   def __getnewargs__(self):
      from abjad.tools import contexttools
      time_signature = contexttools.get_effective_time_signature(self)
      pair = (time_signature.numerator, time_signature.denominator)
      return (pair, )

   def __repr__(self):
      '''String form of measure with parentheses for interpreter display.
      '''
      from abjad.tools import contexttools
      class_name = self.__class__.__name__
      forced_meter = contexttools.get_time_signature_mark_attached_to_component(self)
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
      if len(args) == 1 and isinstance(args[0], contexttools.TimeSignatureMark):
         new_explicit_meter = args[0]
      elif len(args) == 2:
         numerator, denominator = args
         new_explicit_meter = contexttools.TimeSignatureMark(numerator, denominator)
      else:
         raise ValueError('args not understood: "%s".' % str(args))
      partial = kwargs.get('partial', None)
      if partial is not None:
         raise NotImplementedError('partial meter not yet implemented.')
      if contexttools.is_component_with_time_signature_mark_attached(self):
         old_explicit_meter = contexttools.get_time_signature_mark_attached_to_component(self)
         old_explicit_meter.detach_mark( )
      new_explicit_meter(self)

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
      '''True when meter matches duration of measure::

         abjad> measure = Measure((4, 8), "c'8 d'8 e'8 f'8")

      ::

         abjad> measure.is_full
         True

      False otherwise::

         abjad> measure = Measure((4, 8), "c'8 d'8 e'8")

      ::

         abjad> measure.is_full
         False

      Return boolean.
      '''
      return contexttools.get_effective_time_signature(self).duration == self.duration.preprolated
