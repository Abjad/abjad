from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


class _TupletBracketInterface(_Interface, _GrobHandler):
   '''Handle LilyPond TupletBracket grob.'''

   def __init__(self, client):
      '''Bind to client and handle LilyPond TupletBracket grob.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TupletBracket')
