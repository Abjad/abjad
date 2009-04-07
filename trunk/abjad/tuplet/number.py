from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


class _TupletNumberInterface(_Interface, _GrobHandler):
   '''Handle LilyPond TupletNumber grob.'''

   def __init__(self, client):
      '''Bind to client and LilyPond TupletNumber grob.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TupletNumber')
