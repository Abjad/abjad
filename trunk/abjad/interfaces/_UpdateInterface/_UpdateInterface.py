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

   def __init__(self, client):
      '''Initialize update interface.
      '''
      _Interface.__init__(self, client)
      self._allow = True
      self._current = False
      self._observers = set([ ])

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
      
   ## PRIVATE METHODS ## 

   def _allow_component_update(self):
      '''Allow component update after having forbid component update.
      '''
      self._allow = True

   def _forbid_component_update(self):
      '''Temporarily forbid component update.
      '''
      self._allow = False

   def _mark_all_improper_parents_for_update(self):
      '''Mark all all improper parents for update.
      '''
      for x in self._client.parentage.improper_parentage:
         x._update._current = False

   def _update_observer_interfaces_attached_to_all_score_components(self):
      '''Update observer interfaces attached to all score components.
      '''
      from abjad.tools import componenttools
      if not self._all_improper_parents_allow_update:
         return
      score = self._client.parentage.root
      score = componenttools.iterate_components_depth_first(
         score, capped = True, unique = True, forbid = None, direction = 'left')
      for node in score:
         for observer in node._update._observers:
            observer._update_component( )
         node._update._current = True

   def _update_offset_interfaces_attached_to_all_score_components(self):
      '''Update offset interfaces attached to all score components;
      do not update other observer interfaces attached to score components.
      '''
      from abjad.tools import componenttools
      if not self._all_improper_parents_allow_update:
         raise Exception("what's going on here?")
#      score = self._client.parentage.root
#      score = componenttools.iterate_components_depth_first(
#         score, capped = True, unique = True, forbid = None, direction = 'left')
#      for node in score:
#         for observer in node._update._observers:
#            observer._update_component( )
#         node._update._current = True
