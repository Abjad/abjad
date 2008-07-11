from .. core.spanner import _Spanner

class Tie(_Spanner):

   def __init__(self, music):
      _Spanner.__init__(self, music)

   def _right(self, leaf):
      result = [ ]
      if not self._isMyLastLeaf(leaf):
         result.append('~')
      return result
