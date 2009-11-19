from abjad.interfaces.interface.interface import _Interface


class _UpdateInterface(_Interface):
   '''UpdateInterface and OffsetInterface implement the Observer pattern. 
   UpdateInterface holds and updates the state of the branch.
   UpdateInterface holds a list of all the observers.
   UpdateInterface calls ("notifies") all observers to update themselves
   when requested by any observer.
   Observers "pull" the state of the tree from the "subject"
   (UpdateInterface) and tell it to _updateAll( ) if tree has changed.
   '''

   def __init__(self, client):
      '''Bind to client and initialize client as needing update.
      Init empty list of observers.'''
      _Interface.__init__(self, client)
      self._allow = True
      self._current = False
      self._observers = [ ]

   ## PRIVATE ATTRIBUTES ##

   @property
   def _currentToRoot(self):
      '''True if all components in parentage of client are current.'''
      for x in self._client.parentage.parentage:
         if not x._update._current:
            return False
      return True

   @property
   def _allowToRoot(self):
      '''True is all components in parent of client currently allow update.'''
      for x in self._client.parentage.parentage:
         if not x._update._allow:
            return False
      return True
      
   ## PRIVATE METHODS ## 

   def _allowUpdate(self):
      '''Allow update again after having previously forbidden update.'''
      self._allow = True

   def _forbidUpdate(self):
      '''Forbid update until later explicitly allowing update again.'''
      self._allow = False

   def _markForUpdateToRoot(self):
      '''Mark all components in parentage of client as needing update.'''
      for x in self._client.parentage.parentage:
         x._update._current = False

   def _updateAll(self):
      '''Iterate score and call each observer update on each score node.'''
      if self._allowToRoot:
         score = self._client.parentage.root._navigator._DFS( )
         for node in score:
            for observer in node._update._observers:
               observer._update( )
            node._update._current = True
