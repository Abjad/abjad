from abjad.core.interface import _Interface
from abjad.rational.rational import Rational


## TODO: Architectural considerations:
##       This current implementation gives only the _NumberingInterface
##       implemented here and attached to _Component.
##       Would it be better to implement a family of numbering interfaces
##       like _LeafNumberingInterface, _MeasureNumberingInterface, etc.?
##       This family-based approach would mirror the _Formatter classes.
##       Also, right now it is possible to ask for t.numbering.leaf,
##       t.numbering.measure, etc., on *all* components.
##       There's probably nothing wrong with that, but it might be a little
##       weird to ask for t.numbering.leaf when t is a *measure* rather
##       than a leaf.
##       Our more usual way of doing things is to navigate to a single
##       component and ask for attributes there.

class _NumberingInterface(_Interface):

   def __init__(self, _client, updateInterface):
      _Interface.__init__(self, _client)
      self._leaf = 0
      self._measure = 0
      updateInterface._observers.append(self)

   ## PRIVATE METHODS ##

   def _update(self):
      self._updateAllNumbers( )

   ## TODO: Can't this method eliminate all internal navigation?
   def _updateAllNumbers(self):
      from abjad.leaf.leaf import _Leaf
      from abjad.measure.measure import _Measure
      leaf = 0
      measure = 0
      rightwards_dfs = self._client._navigator._DFS(
         direction = 'right', capped = False)
      client = rightwards_dfs.next( )
      for prev in rightwards_dfs:
         if isinstance(prev, _Leaf):
            leaf += 1
         elif isinstance(prev, _Measure):
            measure += 1
      self._leaf = leaf
      self._measure = measure

   ## PUBLIC ATTRIBUTES ##

   @property
   def leaf(self):
      ## TODO: Can't these first three lines be abstracted out?
      update = self._client._update
      if not update._currentToRoot:
         update._updateAll( )
      return self._leaf
   
   @property
   def measure(self):
      ## TODO: Can't these first three lines be abstracted out?
      update = self._client._update
      if not update._currentToRoot:
         update._updateAll( )
      return self._measure
