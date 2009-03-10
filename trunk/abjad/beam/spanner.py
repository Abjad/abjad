from abjad.spanner.grobhandler import _GrobHandlerSpanner


class Beam(_GrobHandlerSpanner):

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'Beam', music)

   ## PRIVATE ATTRIBUTES ##

   def _right(self, leaf):
      '''LilyPond formatting contribution to appear just right of leaf.'''
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append('[')
      if self._isMyLastLeaf(leaf):
         result.append(']')   
      return result
