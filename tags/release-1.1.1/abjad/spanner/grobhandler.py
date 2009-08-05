from abjad.core.grobhandler import _GrobHandler
from abjad.spanner.spanner import Spanner


class _GrobHandlerSpanner(Spanner, _GrobHandler):

   def __init__(self, grob, music = None):
      Spanner.__init__(self, music)
      _GrobHandler.__init__(self, grob)
