from abjad.spanner.positionalhandler import _PositionalGrobHandlerSpanner


class Text(_PositionalGrobHandlerSpanner):

   def __init__(self, music = None):
      _PositionalGrobHandlerSpanner.__init__(self, 'TextSpanner', music)
      self.position = None

   ## PRIVATE ATTRIBUTES ##

   _positions = {'neutral':r'\textSpannerNeutral', 
      'up':r'\textSpannerUp', 'down':r'\textSpannerDown', None:None}

   ## PRIVATE METHODS ##

   def _right(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append(r'\startTextSpan')
      if self._isMyLastLeaf(leaf):
         result.append(r'\stopTextSpan')   
      return result
