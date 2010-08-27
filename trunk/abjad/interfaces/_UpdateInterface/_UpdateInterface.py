from abjad.interfaces._Interface import _Interface


class _UpdateInterface(_Interface):
   '''_UpdateInterface and _ObserverInterface implement the observer pattern. 
   An _UpdateInterface attaches to every Abjad component.
   component._update._current tracks the state of component alone.
   component._update._all_improper_parents_are_current tracks score state.
   component._update._observers is a list of all observer interfaces attached to component.
   component._update_observer_interfaces_attached_to_all_score_components( ) gets called 
   as needed by observer interfaces attached to component.
   '''

   __slots__ = ('_allow', '_current', '_currently_updating', '_observers',
      '_prolated_offset_values_of_component_are_current')
   
   def __init__(self, client):
      '''Initialize update interface.
      '''
      _Interface.__init__(self, client)
      self._allow = True
      self._current = False
      self._currently_updating = False
      self._observers = set([ ])
      self._prolated_offset_values_of_component_are_current = False

   ## PRIVATE ATTRIBUTES ##

   @property
   def _all_improper_parents_are_current(self):
      '''True if all components in improper parentage of client are current.
      '''
      for x in self._client.parentage.improper_parentage:
         if not x._update._current:
            return False
      return True

   @property
   def _all_improper_parents_allow_update(self):
      '''True is all components in improper parent of client currently allow update.
      '''
      for x in self._client.parentage.improper_parentage:
         if not x._update._allow:
            return False
      return True

   @property
   def _any_improper_parents_are_currently_updating(self):
      '''True if any components in improper parentage of client are currently updating.
      '''
      for x in self._client.parentage.improper_parentage:
         if x._update._currently_updating:
            return True
      return False

   @property
   def _prolated_offset_values_of_all_improper_parents_are_current(self):
      for x in self._client.parentage.improper_parentage:
         if not x._update._prolated_offset_values_of_component_are_current:
            return False
      return True
      
   ## PRIVATE METHODS ## 

   def _allow_component_update(self):
      '''Allow component update after having forbid component update.
      '''
      self._allow = True

   def _forbid_component_update(self):
      '''Temporarily forbid component update.
      '''
      self._allow = False

   def _mark_all_improper_parents_as_currently_updating(self):
      '''Mark all improper parents as currently updating.
      '''
      for x in self._client.parentage.improper_parentage:
         x._update._currently_updating = True

   def _mark_all_improper_parents_for_update(self):
      '''Mark all improper parents for update.
      '''
      for x in self._client.parentage.improper_parentage:
         x._update._current = False
         ## important to include the following:
         x._update._prolated_offset_values_of_component_are_current = False

#   def _update_observer_interfaces_attached_to_all_score_components(self):
#      '''Update prolated offset values of all components in a first pass through score.
#      Then update all observer interfaces of all components in a second pass through score.
#      '''
#      if self._all_improper_parents_allow_update:
#         self._update_prolated_offset_values_of_all_score_components( )
#         self._update_observer_interfaces_requiring_prolated_offset_values( )
 
   def _update_observer_interfaces_of_all_score_components(self):
      '''Update observer interfaces of all score components.
      Mark score components as current.
      '''
      #print '(2.) UPDATING OBSERVER INTERFACES OF ALL SCORE COMPONENTS ...'
      from abjad.tools import componenttools
      score = self._client.parentage.root
      score = componenttools.iterate_components_depth_first(
         score, capped = True, unique = True, forbid = None, direction = 'left')
      self._mark_all_improper_parents_as_currently_updating( )
      for node in score:
         for observer in node._update._observers:
            #print node, observer
            observer._update_component( )
         for mark in node.marks:
            mark._bind_effective_context(mark.target_context)
         node._update._currently_updating = False
         node._update._current = True
      ## update offset values of all score components in seconds
      ## only AFTER updating the meter interfaces of all score components
      self.__update_offset_values_of_all_score_components_in_seconds( )

   def __update_offset_values_of_all_score_components_in_seconds(self):
      #print '(3.) UPDATING OFFSET VALUES OF ALL SCORE COMPONENTS IN SECONDS ...' 
      from abjad.tools import componenttools
      score = self._client.parentage.root
      score = componenttools.iterate_components_depth_first(
         score, capped = True, unique = True, forbid = None, direction = 'left')
      for node in score:
         node.offset._update_offset_values_of_component_in_seconds( ) 
      ## no state tracking at close of this method

   def _update_prolated_offset_values_of_all_score_components(self):
      '''Update prolated offset values of offset interfaces attached to all score components;
      do not (yet) update offset values in seconds of any score components;
      do not (yet) update observer interfaces attached to score components;
      do not (yet) mark score components as current.
      '''
      #print '(1.) UPDATING PROLATED OFFSET VALUES OF ALL SCORE COMPONENTS ...' 
      from abjad.tools import componenttools
      score = self._client.parentage.root
      score = componenttools.iterate_components_depth_first(
         score, capped = True, unique = True, forbid = None, direction = 'left')
      for node in score:
         node.offset._update_prolated_offset_values_of_component( ) 
         node._update._prolated_offset_values_of_component_are_current = True
