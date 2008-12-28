#from abjad.spanner.spanner import Spanner
from abjad.spanner.grobhandler import _GrobHandlerSpanner


#class Beam(Spanner):
class Beam(_GrobHandlerSpanner):

   def __init__(self, music = None):
      #Spanner.__init__(self, music)
      _GrobHandlerSpanner.__init__(self, 'Beam', music)

   def _right(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append('[')
      if self._isMyLastLeaf(leaf):
         result.append(']')   
      return result
