from abjad.spanner.spanner import Spanner


class Tie(Spanner):

   def __init__(self, music = None):
      Spanner.__init__(self, music)

   ### TODO Generalize this to work with other like spanner,
   ###      such as Glissando spanner?
   def _captureLeafTies(self):
      '''Capture leaf ties around this Tie spanner.'''
      #leafL = self[0]
      leafL = self.leaves[0]
      prev = leafL.prev
      while prev and prev.tie:
         prev.tie = None
         #self.capture(-1)
         self.insert(0, prev)
         prev = prev.prev

      future =[ ]
      #leafR = self[-1]
      leafR = self.leaves[-1]
      next = leafR.next
      while next and (next.tie or next.prev.tie):
         future.append(next)
         next = next.next
      for leaf in future:
         leaf.tie = None
         self.append(leaf)
      #self.capture(len(future))
         

   ### FORMAT ###

   def _right(self, leaf):
      result = [ ]
      if not self._isMyLastLeaf(leaf):
         result.append('~')
      return result
