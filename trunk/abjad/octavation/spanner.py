from abjad.spanner.spanner import Spanner


class Octavation(Spanner):

   def __init__(self, music = None, start = None, stop = 0):
      Spanner.__init__(self, music)
      self.start = start
      self.stop = stop

   ### TODO - test the shit out of the middleCPosition stuff, esp
   ###        clef changes in the middle of an octavation spanner

   def _before(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append(r'#(set-octavation %s)' % self.start)
      if self._isMyFirstLeaf(leaf) or leaf.clef.change:
         #position = leaf.clef.middleCPosition - 7 * self.start
         position = leaf.clef.effective.middleCPosition - 7 * self.start
         result.append(r'\set Staff.middleCPosition = #%s' % position)
      return result

   def _after(self, leaf):
      result = [ ]
      if self._isMyLastLeaf(leaf):
         result.append(r'#(set-octavation %s)' % self.stop)
         #position = leaf.clef.middleCPosition - 7 * self.stop
         position = leaf.clef.effective.middleCPosition - 7 * self.stop
         result.append(r'\set Staff.middleCPosition = #%s' % position)
      return result
