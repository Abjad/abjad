from abjad.core import _StrictComparator


## TODO: The system model does not clearly define what happens
##       when spanners and forced interface values overlap.
##       What does it mean, for example, when several hundred
##       consecutive notes are spanned with a tempo spanner
##       and when a note somewhere in the middle of the sequence
##       forces a tempo change?

## RESOLVED: _BacktrackingInterface is deprecated in favor of Marks.
##       A number of items in musical score do not model well as spanners.
##       The include clefs, key signatures, time signature, tempo indications
##       instrument name changes and so on. The nature of all of these
##       indications in the score is something like 'from here forward do ...'.
##       This type of indications differs inherently from spanners
##       because spanners are bound at both edges and therefore
##       indicate something like 'from here to here do ...'.

##       All backtracking interfaces are the in the process of being removed.
##       All here-forward sort of score items are now modeled with Marks.
##       No system objects will implement a 'forced' attribute in future.

class _BacktrackingInterface(_StrictComparator):
   '''Mix-in base class for interfaces with 'forced', 'effective' attributes.
   
   Note: class in now DEPRECATED.
   '''

   __slots__ = ( ) ## create real slots definition in concrete child classes

   def __init__(self, _interface_name):
      '''Initialize interface name.'''
      self._interface_name = _interface_name

   ## PRIVATE METHODS ##

   ## TODO: _BacktrackingInterface._get_effective( ) needs extension. ##
   ##       The example below is incorrect and should fix. ##
   
   r'''
   abjad> t = Staff(tuplettools.FixedDurationTuplet((2, 8), macros.scale(3)) * 2)
   abjad> t.leaves[1].clef.forced = stafftools.Clef('bass')
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

   def _get_effective(self):
      '''Works for any interface with 'forced' and 'effective' attributes.
      Most such interfaces are observers.
      '''
      from abjad.components._Leaf import _Leaf
      my_forced = self.forced
      if my_forced is not None:
         return my_forced
      prev_component = self._client._navigator._prev 
      if prev_component is not None:
         if isinstance(prev_component, _Leaf):
            prev_interface = getattr(prev_component, self._interface_name, None)
            if prev_interface is not None:
               prev_forced = prev_interface.forced
               if prev_forced:
                  return prev_forced
               else:
                  return prev_interface._effective
         else:
            ## TODO: this is a hack; the logic here will work if prev
            ##       component is a container that happens to contain
            ##       a leaf as its last contained element.
            ##       The logic here needs to be truly backwards recursive.
            ## TODO: Using componenttools.iterate_components_depth_first( ) 
            ##       here *backwards* should work.
            try:
               last_contained = prev_component[-1]
            except IndexError:
               last_contained = prev_component
            prev_interface = getattr(last_contained, self._interface_name, None)
            if prev_interface is not None:
               prev_forced = prev_interface.forced
               if prev_forced:
                  return prev_forced
               else:
                  return prev_interface._effective
      for parent in self._client.parentage.proper_parentage:
         parent_interface = getattr(parent, self._interface_name, None)
         if parent_interface is not None:
            parent_forced = parent_interface.forced
            if parent_forced is not None:
               return parent_forced
      default = getattr(self, 'default', None)
      return default
   
   def _update_component(self):
      '''Update my score-dependent core attributes.'''
      effective = self._get_effective( )
      self._effective = effective

   ## PUBLIC ATTRIBUTES ##

   @property
   def change(self):
      '''True when core attribute changes at client, otherwise False.'''
      prev_leaf = getattr(self._client, 'prev', None)
      if prev_leaf:
         prev_interface = getattr(prev_leaf, self._interface_name)
         cur_interface = getattr(self._client, self._interface_name)
         return not prev_interface.effective == cur_interface.effective
      return False

   @property
   def effective(self):
      '''Effective core attribute governing client.'''
      forced = self._forced
      if forced is not None:
         return forced
      else:
         #self._update_all_observer_interfaces_in_score_if_necessary( )
         self._update_prolated_offset_values_of_all_score_components_if_necessary( )
         self._update_observer_interfaces_of_all_score_components_if_necessary( )
      return self._effective

   @apply
   def forced( ):
      '''Read / write core attribute explicitly.'''
      def fget(self):
         return self._forced
      def fset(self, arg):
         assert isinstance(arg, (self._acceptable_types, type(None)))
         self._forced = arg
         self._client._update._mark_all_improper_parents_for_update( )
      return property(**locals( ))
