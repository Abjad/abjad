from abjad.core.grobhandler import _GrobHandler
from abjad.spanner.spanner import Spanner


class _GrobHandlerSpanner(Spanner, _GrobHandler):

   def __init__(self, grob, music = None):
      Spanner.__init__(self, music)
      _GrobHandler.__init__(self, grob)

#   ## PUBLIC METHODS ##
#
#   def after(self, component):
#      result = [ ]
#      if self._isMyLastLeaf(component):
#         result.extend(self.reverts)
#      return result
#
#   def before(self, component):
#      result = [ ]
#      if self._isMyFirstLeaf(component):
#         result.extend(self.overrides)
#      return result
