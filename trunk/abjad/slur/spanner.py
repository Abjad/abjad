from abjad.spanner.grobhandler import _GrobHandlerSpanner


class Slur(_GrobHandlerSpanner):

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'Slur', music)

   def _right(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append('(')
      if self._isMyLastLeaf(leaf):
         result.append(')')   
      return result
