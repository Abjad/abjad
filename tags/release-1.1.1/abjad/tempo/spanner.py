from abjad.exceptions import UndefinedSpacingError
from abjad.exceptions import UndefinedTempoError
from abjad.rational import Rational
from abjad.spanner.grobhandler import _GrobHandlerSpanner
from abjad.tempo.format import _TempoSpannerFormatInterface
from abjad.tempo.indication import TempoIndication
import types


class Tempo(_GrobHandlerSpanner):
   r'''Apply tempo indication to zero or more contiguous components.

   Handle LilyPond ``MetronomeMark`` grob.

   Handle LilyPond ``proportionalNotationDuration`` context setting.

   Invoke LilyPond ``\newSpacingSection`` command.
   '''

   def __init__(self, music = None, indication = None):
      '''Handle LilyPond MetronomeMark grob. Init tempo indication.'''

      _GrobHandlerSpanner.__init__(self, 'MetronomeMark', music)
      self._format = _TempoSpannerFormatInterface(self)
      self._proportional_notation_duration_effective = None
      self._proportional_notation_duration_reference = None
      self.indication = indication
      self.reference = None

   ## OVERRIDES ##

   def __repr__(self):
      name = self.__class__.__name__
      summary = self._summary
      if self.indication is not None:
         equation = self.indication._equation
         return '%s(%s, %s)' % (name, equation, summary)
      else:
         return '%s(%s)' % (name, summary) 

   ## PUBLIC ATTRIBUTES ##

   @apply
   def indication( ):
      def fget(self):
         '''Read / write tempo indication.'''
         return self._indication
      def fset(self, arg):
         assert isinstance(arg, (TempoIndication, types.NoneType))
         if isinstance(arg, TempoIndication):
            self._indication = TempoIndication(arg)
         elif isinstance(arg, types.NoneType):
            self._indication = arg 
         else:
            raise ValueError('must be Abjad TempoIndication or None.')
      return property(**locals( ))

   @property
   def proportional_notation_duration_effective(self):
      '''Read-only LilyPond proportionalNotationDuration.
      Raises UndefinedTempoError if reference tempo undefined.
      Raises UndefinedSpacingError if reference spacing undefined.

      .. todo:: Write Tempo.proportional_notation_duration_effective( )
         tests.
      '''
      reference = self.proportional_notation_duration_reference
      if reference is not None:
         return self.scaling_factor * reference
      raise UndefinedSpacingError

   @apply
   def proportional_notation_duration_reference( ):
      def fget(self):
         '''Read / write LilyPond proportionalNotationDuration. \
         Must be rational-valued duration.

         .. todo:: Write Tempo.proportional_notation_duration_reference( )
            tests.
         '''
         return self._proportional_notation_duration_reference
      def fset(self, arg):
         assert isinstance(arg, Rational)
         assert 0 < arg
         self._proportional_notation_duration_reference = arg
      return property(**locals( ))

   @apply
   def reference( ):
      def fget(self):
         '''Read / write reference tempo indication. \
         If set, scale durations at format-time.'''
         return self._reference
      def fset(self, arg):
         assert isinstance(arg, (TempoIndication, types.NoneType))
         self._reference = arg 
      return property(**locals( ))

   @property
   def scaling_factor(self):
      '''Reference tempo divided by indicated tempo.'''
      try:
         return self.reference.maelzel / self.indication.maelzel
      except AttributeError:
         raise UndefinedTempoError
