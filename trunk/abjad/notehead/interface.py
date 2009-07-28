from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


class NoteHeadInterface(_Interface, _GrobHandler):
   '''Handle LilyPond NoteHead grob.'''

   def __init__(self, client):
      '''Bind client and LilyPond NoteHead grob.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'NoteHead')

   ## PUBLIC ATTRIBUTES ##

   ## TODO: This is an (effective) hack to filter out any erroneous
   ##       \once \override NoteHead #'pitch = #'cs
   ##       that NoteHeadInterface might contribute.

   @property
   def _overrides(self):
      result = [ ]
      result.extend(_GrobHandler._overrides.fget(self))
      result = [x for x in result if not "#'pitch" in x]
      return result
