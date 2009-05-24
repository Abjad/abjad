from abjad.context.context import _Context


class Score(_Context):
   '''*Abjad* model of the musical score.'''

   def __init__(self, music = None):
      '''Init score as type of *Abjad* container.
         Init ``context`` to ``Score`` and ``parallel`` to ``True``.'''
      _Context.__init__(self, music)
      self.context = 'Score'
      self.parallel = True
