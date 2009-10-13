from abjad.context.context import _Context
from abjad.tools.spacing import SpacingIndication
import types


class Score(_Context):
   '''Abjad model of the musical score.'''

   def __init__(self, music = None):
      '''Init score as type of Abjad container.
      Init ``context`` to ``Score`` and ``parallel`` to ``True``.'''
      _Context.__init__(self, music)
      self.context = 'Score'
      self.global_spacing = None
      self.parallel = True

   ## PUBLIC ATTRIBUTES ##

   @apply
   def global_spacing( ):
      def fget(self):
         '''Special read / write attribute to manage score-global spacing.

         Assign Abjad :class:`~abjad.SpacingIndication` or ``None``.

         Set to activate Abjad :class:`~abjad.TempoProportional` spanners.

         .. todo:: Encapsulate in SpacingInterface.
         '''
         return self._global_spacing
      def fset(self, expr):
         assert isinstance(expr, (SpacingIndication, types.NoneType))
         self._global_spacing = expr
      return property(**locals( ))
