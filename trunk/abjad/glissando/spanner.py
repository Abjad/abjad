from .. core.spanner import _Spanner

class Glissando(_Spanner):

   def __init__(self, leaves):
      _Spanner.__init__(self, leaves)

   def _right(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append(r'\glissando')
      if self._isMyLastLeaf(leaf):
         result.append(r'%% end of glissando')
      return result
