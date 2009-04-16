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
      _BacktrackingInterface.__init__(self, 'clef.name')
      self._effectiveName = 'treble'
      self._forced = None

   ## PRIVATE METHODS ##

   def _update(self):
      '''Update my score-dependent clef attributes.'''
      self._updateEffectiveClefName( )

   def _updateEffectiveClefName(self):
      '''Update my effective clef.'''
      myForced = self.forced
      if myForced is not None:
         self._effectiveName = myForced.name
      elif self._client._navigator._prev is not None:
         prevComponent = self._client._navigator._prev
         if prevComponent:
            prevForced = prevComponent.clef.forced
            if prevForced:
               self._effectiveName = prevForced.name
            else:
               prevEffectiveName = prevComponent.clef._effectiveName
               self._effectiveName = prevEffectiveName
      else:
         for parent in self._client.parentage.parentage[1:]:
            parentForced = parent.clef.forced
            if parentForced is not None:
               self._effectiveName = parentForced.name
               break

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective(self):
      '''Return effective clef or else treble.'''
      self._makeSubjectUpdateIfNecessary( )
      return Clef(self._effectiveName)

   @apply
   def forced( ):
      '''Forced clef change here.'''
      def fget(self):
         return self._forced
      def fset(self, arg):
         assert isinstance(arg, (Clef, types.NoneType))
         self._forced = arg
      return property(**locals( ))

   @property
   def opening(self):
      '''Format contribution at container opening or before leaf.'''
      result = [ ]
      if self.forced or self.change:
         result.append(self.effective.format)
      return result
