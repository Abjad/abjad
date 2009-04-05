from abjad.spanner.positionalhandler import _PositionalGrobHandlerSpanner
from abjad.text.format import _TextSpannerFormatInterface


class Text(_PositionalGrobHandlerSpanner):

   def __init__(self, music = None):
      _PositionalGrobHandlerSpanner.__init__(self, 'TextSpanner', music)
      self._format = _TextSpannerFormatInterface(self)
      self.position = None

   ## PRIVATE ATTRIBUTES ##

   _positions = {'neutral':r'\textSpannerNeutral', 
      'up':r'\textSpannerUp', 'down':r'\textSpannerDown', None:None}

#   ## PUBLIC METHODS ##
#
#   def right(self, leaf):
#      result = [ ]
#      if self._isMyFirstLeaf(leaf):
#         result.append(r'\startTextSpan')
#      if self._isMyLastLeaf(leaf):
#         result.append(r'\stopTextSpan')   
#      return result
