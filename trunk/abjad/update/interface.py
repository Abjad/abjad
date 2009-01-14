from abjad.core.interface import _Interface
from abjad.rational.rational import Rational

### UpdateInterface and OffsetInterface implement the Observer pattern. 
### UpdateInterface holds and updates the state of the branch.
### UpdateInterface holds a list of all the observers.
### UpdateInterface calls ("notifies") all observers to update themselves
### when requested by any observer.
### Observers "pull" the state of the tree from the "subject" 
### (UpdateInterface) and tell it to updateAll( ) if tree has changed.


class _UpdateInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      self._current = False
      self._observers = [ ]

   ### PRIVATE ATTRIBUTES ###

   @property
   def _currentToRoot(self):
      #for x in self._client._parentage._parentage:
      #for x in self._client.parentage._parentage:
      for x in self._client.parentage.parentage:
         if not x._update._current:
            return False
      return True
      
   ### PRIVATE METHODS ### 

   def _markForUpdateToRoot(self):
      #for x in self._client._parentage._parentage:
      #for x in self._client.parentage._parentage:
      for x in self._client.parentage.parentage:
         x._update._current = False

#   def _updateAll(self):
#      g = self._client._parentage._root._navigator._DFS( )
#      score_offset = Rational(0)
#      for node in g:
#         if node.kind('_Leaf'):
#            node.offset._special = score_offset
#            score_offset += node.duration.prolated
#         node._update._current = True

   def _updateAll(self):
      #g = self._client._parentage._root._navigator._DFS( )
      #g = self._client.parentage._root._navigator._DFS( )
      g = self._client.parentage.root._navigator._DFS( )
      for node in g:
         for o in node._update._observers:
            o.update( )
         node._update._current = True
