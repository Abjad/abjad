from abjad.core.abjadcore import _Abjad


## TODO: The system model does not clearly define what happens
##       when spanners and forced interface values overlap.
##       What does it mean, for example, when several hundred
##       consecutive notes are spanned with a tempo spanner
##       and when a note somewhere in the middle of the sequence
##       forces a tempo change?

##       The solution implemented as of r2125 is that spanners will
##       'win' in place of forced and backtracked attributes.
##       That is, in the example above, all notes governed by the
##       hypothetical tempo spanner will derive t.tempo.effective
##       directly from the governing spanner EXCEPT for the
##       one note in the middle of a run one which the tempo is forced.

## NOTE: This solution is not evident here in _BacktrackingInterface.
##       You have to look at, for example, TempoInterface.effective
##       to see the logic that determines who wins the tournament.

class _BacktrackingInterface(_Abjad):
   '''Mixin base class for interfaces with 'forced', 'effective' attributes.'''

   def __init__(self, _interfaceName):
      '''Initialize interface name.'''
      self._interfaceName = _interfaceName

   ## PRIVATE METHODS ##

   ## TODO: Can _BacktrackingInterface._getEffective( ) deprecate? ##

   def _getEffective(self):
      '''Works for any interface with 'forced' and 'effective' attributes.
         Most such interfaces are observers.'''
      myForced = self.forced
      if myForced is not None:
         return myForced
      prevComponent = self._client._navigator._prev 
      if prevComponent is not None:
         prevInterface = getattr(prevComponent, self._interfaceName, None)
         if prevInterface is not None:
            prevForced = prevInterface.forced
            if prevForced:
               return prevForced
            else:
               return prevInterface._effective
      for parent in self._client.parentage.parentage[1:]:
         parentInterface = getattr(parent, self._interfaceName, None)
         if parentInterface is not None:
            parentForced = parentInterface.forced
            if parentForced is not None:
               return parentForced
      default = getattr(self, 'default', None)
      return default
   
   def _update(self):
      '''Update my score-dependent core attributes.'''
      effective = self._getEffective( )
      self._effective = effective

   ## PUBLIC ATTRIBUTES ##

   @property
   def change(self):
      '''True when core attribute changes at client, otherwise False.'''
      prevLeaf = getattr(self._client, 'prev', None)
      if prevLeaf:
         prevInterface = getattr(prevLeaf, self._interfaceName)
         curInterface = getattr(self._client, self._interfaceName)
         return not prevInterface.effective == curInterface.effective
      return False

   @property
   def effective(self):
      '''Effective core attribute governing client.'''
      forced = self._forced
      if forced is not None:
         return forced
      else:
         self._makeSubjectUpdateIfNecessary( )
         return self._effective

   @apply
   def forced( ):
      '''Read / write core attribute explicitly.'''
      def fget(self):
         return self._forced
      def fset(self, arg):
         assert isinstance(arg, self._acceptableTypes)
         self._forced = arg
         self._client._update._markForUpdateToRoot( )
      return property(**locals( ))
