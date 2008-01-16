from .. core.spanner import _Spanner

class Octavation(_Spanner):

   def __init__(self, leaves, start, stop = 0):
      _Spanner.__init__(self, leaves)
      self.start = start
      self.stop = stop

   def _before(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append(r'#(set-octavation %s)' % self.start)
         #if leaf.clef.name != 'treble':
         #   position = leaf.clef.middleCPosition - 7 * self.start
         #   result.append(r'\set Staff.middleCPosition = #%s' % position)
      return result

   def _after(self, leaf):
      result = [ ]
      if self._isMyLastLeaf(leaf):
         result.append(r'#(set-octavation %s)' % self.stop)
         #if self.leaves[0].clef.name != 'treble':
         #   result.append(r'\set Staff.middleCPosition = #%s' % 
         #      leaf.clef.middleCPosition)
      return result
