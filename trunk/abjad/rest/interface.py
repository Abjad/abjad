from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces.interface.interface import _Interface


class RestInterface(_Interface, _GrobHandler):
   '''Handle LilyPond Rest grob.'''

   def __init__(self, client):
      '''Bind to client and LilyPond Rest grob.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Rest')
