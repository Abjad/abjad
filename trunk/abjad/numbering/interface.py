from abjad.core.observer import _Observer
from abjad.exceptions.exceptions import MeasureContiguityError
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

class _NumberingInterface(_Observer):
   '''Number score components and handle no LilyPond grob.'''

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
         self._leaf = prevLeaf.numbering.leaf + 1

   def _updateMeasureNumber(self):
      '''Update (one-indexed) number of any one measure in score.'''
      from abjad.tools import iterate
      try:
         prev = iterate.measure_prev(self._client)
         self._measure = prev.numbering.measure + 1
      except StopIteration:
         pass

   ## PUBLIC ATTRIBUTES ##

   @property
   def leaf(self):
      '''(Zero-indexed) number of leaf in score.'''
      self._makeSubjectUpdateIfNecessary( )
      return self._leaf
   
   @property
   def measure(self):
      '''(One-indexed) number of measure in score.'''
      self._makeSubjectUpdateIfNecessary( )
      return self._measure
