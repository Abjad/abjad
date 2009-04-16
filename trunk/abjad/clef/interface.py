from abjad.clef.clef import Clef
from abjad.core.backtracking import _BacktrackingInterface
from abjad.core.grobhandler import _GrobHandler
from abjad.core.observer import _Observer
import types


class _ClefInterface(_Observer, _GrobHandler, _BacktrackingInterface):
   '''Handle LilyPond Clef grob.
      Observe score structure to find effective clef.
      Manage forced clef changes.'''
   
   def __init__(self, _client, updateInterface):
      '''Bind client and LilyPond Clef grob.
         Set forced to None.'''
      _Observer.__init__(self, _client, updateInterface)
      _GrobHandler.__init__(self, 'Clef')
      _BacktrackingInterface.__init__(self, 'clef')
      self._acceptableTypes = (Clef, types.NoneType)
      self._effective = Clef('treble')
      self._forced = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def opening(self):
      '''Format contribution at container opening or before leaf.'''
      result = [ ]
      if self.forced or self.change:
         result.append(self.effective.format)
      return result
