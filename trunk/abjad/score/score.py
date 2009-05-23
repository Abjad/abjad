from abjad.context.context import _Context


class Score(_Context):
   '''*Abjad* model of the *LilyPond* ``score`` context.'''

   def __init__(self, music = None):
      '''Initialize parallel score context.'''
      music = music or [ ]
      _Context.__init__(self, music)
      self.parallel = True
      self.context = 'Score'
