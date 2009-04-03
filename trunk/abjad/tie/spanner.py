from abjad.spanner.grobhandler import _GrobHandlerSpanner


class Tie(_GrobHandlerSpanner):

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'Tie', music)

   ## PUBLIC METHODS ##

   def right(self, leaf):
      result = [ ]
      if not self._isMyLastLeaf(leaf):
         result.append('~')
      return result
