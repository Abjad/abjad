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
      self._default = Clef('treble')
      self._forced = None
      self._suppress = False

   ## TODO: Generalize _selfShouldContribute for both _Clef and _Meter ##

   ## PRIVATE ATTRIBUTES ##

   @property
   def _selfCanContribute(self):
      r'''True when self is able to contribute LilyPond \clef.'''
      return not self.suppress and (self.forced or self.change)

   @property
   def _selfShouldContribute(self):
      r'''True when self should contribute LilyPond \clef.'''
      return self._selfCanContribute and not self._parentCanContribute

   @property
   def _parentCanContribute(self):
      r'''True when any parent, other than self, can contribute LP \clef.'''
      #for parent in self.client.parentage.parentage[1:]:
      for parent in self._client.parentage.parentage[1:]:
         try:
            if parent.clef._selfCanContribute:
               return True
         except AttributeError:
            pass
      return False

   ## PUBLIC ATTRIBUTES ##

   @property
   def default(self):
      return self._default

   @property
   def opening(self):
      '''Format contribution at container opening or before leaf.'''
      result = [ ]
      #if self.forced or self.change:
      if self._selfShouldContribute:
         result.append(self.effective.format)
      return result

   @apply
   def suppress( ):
      r'''Read / write attribute to suppress contribution
         of LilyPond \clef indication at format-time.'''
      def fget(self):
         return self._suppress
      def fset(self, arg):
         assert isinstance(arg, (bool, types.NoneType))
         self._suppress = arg
      return property(**locals( ))
