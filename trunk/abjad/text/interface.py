from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


class _TextInterface(_Interface, _GrobHandler):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TextScript')

   ### PRIVATE ATTRIBUTES ###

   ### NOTE: kinda kinky

   @property
   def _opening(self):
      return self._before
