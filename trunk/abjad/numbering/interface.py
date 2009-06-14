from abjad.core.observer import _Observer
from abjad.exceptions.exceptions import MeasureContiguityError
from abjad.rational import Rational


class _NumberingInterface(_Observer):
   '''Number score components but handle no LilyPond grob.'''

   def __init__(self, _client, updateInterface):
      '''Bind to client and register self as observer.
         Init leaf and measure numbers to zero.'''
      _Observer.__init__(self, _client, updateInterface)
      self._leaf = 0
      self._measure = 1

   ## PRIVATE METHODS ##

   def _update(self):
      '''Update number of any one node in score.'''
      from abjad.leaf.leaf import _Leaf
      from abjad.measure.measure import _Measure
      client = self._client
      if isinstance(client, _Leaf):
         self._updateLeafNumber( )
      elif isinstance(client, _Measure):
         self._updateMeasureNumber( )

   def _updateLeafNumber(self):
      '''Update (zero-indexed) number of any one leaf in score.'''
      from abjad.leaf.leaf import _Leaf
      prevLeaf = self.client.prev
      if prevLeaf:
         assert isinstance(prevLeaf, _Leaf)
         self._leaf = prevLeaf._numbering._leaf + 1
      else:
         self._leaf = 0

   def _updateMeasureNumber(self):
      '''Update (one-indexed) number of any one measure in score.'''
      from abjad.tools import iterate
#      try:
#         prev = iterate.measure_prev(self._client)
#         self._measure = prev._numbering._measure + 1
#      except StopIteration:
#         self._measure = 1
      prevMeasure = iterate.measure_prev(self._client)
      if prevMeasure is not None:
         self._measure = prevMeasure._numbering._measure + 1
      else:
         self._measure = 1
