from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface

 
class _StemInterface(_Interface, _GrobHandler):
   '''Handle LilyPond Stem grob.'''

   def __init__(self, client):
      '''Bind to client and LilyPond Stem grob.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Stem')
