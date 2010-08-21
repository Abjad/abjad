from abjad.core import _BacktrackingInterface
from abjad.core import _Observer


class ClefInterface(_Observer, _BacktrackingInterface):
   '''Observe score structure to find effective clef.
   Manage forced clef changes.
   '''
   
   def __init__(self, _client, updateInterface):
      from abjad.tools.stafftools import Clef
      _Observer.__init__(self, _client, updateInterface)
      _BacktrackingInterface.__init__(self, 'clef')
      self._acceptableTypes = (Clef, )
      self._default = Clef('treble')
      self._forced = None
      #self._suppress = False
      self._suppress = None

   ## TODO: Generalize _self_should_contribute for both _Clef and _Meter ##

   ## PRIVATE ATTRIBUTES ##

   @property
   def _self_can_contribute(self):
      r'''True when self is able to contribute LilyPond \clef.'''
      return not self.suppress and (self.forced or self.change)

   @property
   def _self_should_contribute(self):
      r'''True when self should contribute LilyPond \clef.'''
      return self._self_can_contribute and not self._parent_can_contribute

   @property
   def _parent_can_contribute(self):
      r'''True when any parent, other than self, can contribute LP \clef
      and when that parent begins at the exact same moment as client,
      effectively overruling forced clef of client.
      '''
      for parent in self._client.parentage.parentage[1:]:
         try:
            if parent.clef._self_can_contribute:
               if self._client in \
                  parent._navigator._contemporaneous_start_components:
                  return True
         except AttributeError:
            pass
      return False

   ## PUBLIC ATTRIBUTES ##

   @property
   def default(self):
      return self._default

   @property
   def _opening(self):
      '''Format contribution at container opening or before leaf.'''
      result = [ ]
      #if self.forced or self.change:
      if self._self_should_contribute:
         result.append(self.effective.format)
      return result

   @apply
   def suppress( ):
      r'''Read / write attribute to suppress contribution
         of LilyPond \clef indication at format-time.'''
      def fget(self):
         return self._suppress
      def fset(self, arg):
         assert isinstance(arg, (bool, type(None)))
         self._suppress = arg
      return property(**locals( ))
