from abjad.core.interface import _Interface
from abjad.rational.rational import Rational


class _UpdateInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      self._current = False

   ### PRIVATE ATTRIBUTES ###

   @property
   def _currentToRoot(self):
      for x in self._client._parentage._iparentage:
         if not x._update._current:
            return False
      return True
      
   ### PRIVATE METHODS ### 

   def _markForUpdateToRoot(self):
      for x in self._client._parentage._iparentage:
         x._update._current = False

   def _updateAll(self):
      g = self._client._parentage._root._navigator._DFS( )
      score_offset = Rational(0)
      for node in g:
         if node.kind('_Leaf'):
            node.offset._special = score_offset
            score_offset += node.duration.prolated
         node._update._current = True
