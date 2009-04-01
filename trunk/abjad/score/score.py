from abjad.context.context import _Context


class Score(_Context):

   def __init__(self, music = None):
      music = music or [ ]
      _Context.__init__(self, music)
      self.parallel = True
      self.context = 'Score'

   ## PUBLIC METHODS ##

   def setCurrentBarNumber(self, n):
      currentBarNumber = r"\set Score.currentBarNumber = #%s" % n
      self.leaves[0].before.append(currentBarNumber)
