from abjad.interfaces._Interface import _Interface


class _UpdateInterface(_Interface):
   '''_UpdateInterface and _ObserverInterface implement the observer pattern. 
   An _UpdateInterface attaches to every Abjad component.
   component._update._current tracks the state of component alone.
   component._update._current_to_root tracks score state.
   component._update._observers is a list of all observer interfaces attached to component.
   component._update_all( ) updates all observer interfaces attached to component.
   component._update_all( ) gets called as needed by observer interfaces attached to component.
   '''

   def __init__(self, client):
      '''Initialize update interface.
      '''
      _Interface.__init__(self, client)
      self._allow = True
      self._current = False
      self._observers = [ ]

   ## PRIVATE ATTRIBUTES ##

   @property
   def _current_to_root(self):
      '''True if all components in improper parentage of client are current.
      '''
      for x in self._client.parentage.improper_parentage:
         if not x._update._current:
            return False
      return True

   @property
   def _allow_to_root(self):
      '''True is all components in improper parent of client currently allow update.
      '''
      for x in self._client.parentage.improper_parentage:
         if not x._update._allow:
            return False
      return True
      
   ## PRIVATE METHODS ## 

   def _allow_update(self):
      '''Allow component update again after having previously forbidden component update.
      '''
      self._allow = True

   def _forbid_update(self):
      '''Temporarily Forbid component update.
      '''
      self._allow = False

   def _mark_for_update_to_root(self):
      '''Mark all components in improper parentage of client as needing update.
      '''
      for x in self._client.parentage.improper_parentage:
         x._update._current = False

   def _update_all(self):
      '''Iterate score and update the observer interfaces attached to every node in score.
      '''
      from abjad.tools import componenttools
      if self._allow_to_root:
         score = self._client.parentage.root
         score = componenttools.iterate_components_depth_first(
            score, capped = True, unique = True, forbid = None, direction = 'left')
         for node in score:
            for observer in node._update._observers:
               observer._update( )
            node._update._current = True
