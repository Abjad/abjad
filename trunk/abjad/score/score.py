from abjad.context.context import _Context
from abjad.interfaces.spacing.score.interface import ScoreSpacingInterface
from abjad.tools.spacing import SpacingIndication
import types


class Score(_Context):
   '''Abjad model of the musical score.'''

   def __init__(self, music = None):
      '''Init score as type of Abjad container.
      Init ``context`` to ``Score`` and ``parallel`` to ``True``.'''
      _Context.__init__(self, music)
      self._spacing = ScoreSpacingInterface(self)
      self.context = 'Score'
      self.parallel = True

   ## PUBLIC ATTRIBUTES ##

   @property
   def spacing(self):
      '''Read-only reference to
      :class:`~abjad.spacing.score.interface.ScoreSpacingInterface`.'''
      return self._spacing
