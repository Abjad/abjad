from abjad.spanner.grobhandler import _GrobHandlerSpanner


class Glissando(_GrobHandlerSpanner):

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'Glissando', music)

   ## PRIVATE METHODS ##

   def _right(self, leaf):
      result = [ ]
      if not self._isMyLastLeaf(leaf):
         result.append(r'\glissando')
      return result
