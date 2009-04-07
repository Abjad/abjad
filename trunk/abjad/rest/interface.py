from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


class _RestInterface(_Interface, _GrobHandler):
   '''Handle LilyPond Rest grob.'''

   def __init__(self, client):
      '''Bind to client and LilyPond Rest grob.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Rest')
