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

import types


class _BacktrackingInterface(_Abjad):
   '''Mixin base class for interfaces with 'forced', 'effective' attributes.'''

   def __init__(self, _interfaceName):
      '''Initialize interface name.'''
      self._interfaceName = _interfaceName

   ## PRIVATE METHODS ##

   ## TODO: _BacktrackingInterface._getEffective( ) needs extension. ##
   ##       The example below is incorrect and should fix. ##
   
   r'''
   abjad> t = Staff(FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3)) * 2)
   abjad> t.leaves[1].clef.forced = Clef('bass')
   \new Staff {
           \times 2/3 {
                   c'8
                   \clef "bass"
                   d'8
                   e'8
           }
           \times 2/3 {
                   \clef "treble"
                   c'8
                   d'8
                   e'8
           }
   }
   '''

   def _getEffective(self):
      '''Works for any interface with 'forced' and 'effective' attributes.
         Most such interfaces are observers.'''
      from abjad.tools import iterate
      from abjad.leaf import _Leaf
      myForced = self.forced
      if myForced is not None:
         return myForced
      prevComponent = self._client._navigator._prev 
      if prevComponent is not None:
#         prevInterface = getattr(prevComponent, self._interfaceName, None)
#         if prevInterface is not None:
#            prevForced = prevInterface.forced
#            if prevForced:
#               return prevForced
#            else:
#               return prevInterface._effective
         if isinstance(prevComponent, _Leaf):
            prevInterface = getattr(prevComponent, self._interfaceName, None)
            if prevInterface is not None:
               prevForced = prevInterface.forced
               if prevForced:
                  return prevForced
               else:
                  return prevInterface._effective
         else:
            ## TODO: this is a hack; the logic here will work if prev
            ##       component is a container that happens to contain
            ##       a leaf as its last contained element.
            ##       The logic here needs to be truly backwards recursive.
            ## TODO: Using iterate.depth_first( ) here *backwards* should work.
            try:
               last_contained = prevComponent[-1]
            except IndexError:
               last_contained = prevComponent
            prevInterface = getattr(last_contained, self._interfaceName, None)
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
         assert isinstance(arg, (self._acceptableTypes, types.NoneType))
         self._forced = arg
         self._client._update._markForUpdateToRoot( )
      return property(**locals( ))
