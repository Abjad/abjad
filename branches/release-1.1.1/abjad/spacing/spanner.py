from abjad.spacing.format import _SpacingSpannerFormatInterface
from abjad.spanner.grobhandler import _GrobHandlerSpanner
import types


class SpacingSpanner(_GrobHandlerSpanner):
   r'''Model a spacing section of musical score.

   Handle LilyPond ``SpacingSpanner`` grob.

   Handle LilyPond ``\newSpacingSection`` command.
   '''

   def __init__(self, music = None):
      r'''Handle LilyPond ``SpacingSpanner`` grob.
      Handle LilyPond ``\newSpacingSection`` command.
      Init ``new_section`` as ``None``.
      '''

      _GrobHandlerSpanner.__init__(self, 'SpacingSpanner', music)
      self._format = _SpacingSpannerFormatInterface(self)
      self.new_section = None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def new_section( ):
      def fget(self):
         r'''Read / write interface to LilyPond 
         ``\newSpacingSection`` command.

         Set to ``True``, ``False`` or ``None``.
         '''
         return self._new_section
      def fset(self, expr):
         assert isinstance(expr, (bool, types.NoneType))
         self._new_section = expr
      return property(**locals( ))
