from abjad.spanner.grobhandler import _GrobHandlerSpanner
from abjad.tie.format import _TieSpannerFormatInterface


class Tie(_GrobHandlerSpanner):

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'Tie', music)
      self._format = _TieSpannerFormatInterface(self)

#   ## PUBLIC METHODS ##
#
#   def right(self, leaf):
#      result = [ ]
#      if not self._isMyLastLeaf(leaf):
#         result.append('~')
#      return result
