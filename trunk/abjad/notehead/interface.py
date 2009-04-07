from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


class _NoteHeadInterface(_Interface, _GrobHandler):
   '''Handle LilyPond NoteHead grob.'''

   def __init__(self, client):
      '''Bind client and LilyPond NoteHead grob.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'NoteHead')
