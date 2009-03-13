from abjad.context.context import _Context


class Score(_Context):

   def __init__(self, music = None):
      music = music or [ ]
      _Context.__init__(self, music)
      self.brackets = 'double-angle'
      self.invocation = 'Score'

   ## PUBLIC METHODS ##

   ## TODO - insert measure and breaks voices at format-time ##

   def setCurrentBarNumber(self, n):
      currentBarNumber = r"\set Score.currentBarNumber = #%s" % n
      self.leaves[0].before.append(currentBarNumber)
