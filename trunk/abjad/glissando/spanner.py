from abjad.spanner.grobhandler import _GrobHandlerSpanner


class Glissando(_GrobHandlerSpanner):

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'Glissando', music)

   ## PUBLIC METHODS ##

   def right(self, leaf):
      result = [ ]
      if not self._isMyLastLeaf(leaf):
         result.append(r'\glissando')
      return result
