from abjad.articulations.interface import _ArticulationsInterface
from abjad.clef.clef import Clef
from abjad.component.component import _Component
from abjad.core.interface import _Interface
from abjad.grace.interface import _GraceInterface
from abjad.harmonic.interface import _HarmonicInterface
from abjad.leaf.duration import _LeafDurationInterface
from abjad.leaf.formatter import _LeafFormatter
from abjad.leaf.spanner.aggregator import _LeafSpannerAggregator
from abjad.markup.interface import _MarkupInterface
from abjad.parentage.parentage import _Parentage
from abjad.rational.rational import Rational
from abjad.staff.interface import _StaffInterface
import operator


class _Leaf(_Component):

   def __init__(self, duration):
      _Component.__init__(self)
      self._parentage = _Parentage(self)
      self._articulations = _ArticulationsInterface(self)
      self._duration = _LeafDurationInterface(self, duration)
      self._formatter = _LeafFormatter(self)
      self._grace = _GraceInterface(self)
      self._harmonic = _HarmonicInterface(self)
      self._history = { }
      self._markup = _MarkupInterface(self)
      self._spanners = _LeafSpannerAggregator(self)
      self._staff = _StaffInterface(self)

   ## OVERLOADS ##

   def __and__(self, arg):
      return self._operate(arg, operator.__and__)

   def __or__(self, arg):
      return self._operate(arg, operator.__or__)

   def __sub__(self, arg):
      return self._operate(arg, operator.__sub__)

   def __xor__(self, arg):
      return self._operate(arg, operator.__xor__)

   ## PRIVATE METHODS ##

   def _operate(self, arg, operator):
      assert isinstance(arg, _Leaf)
      from abjad.helpers.engender import engender
      pairs = operator(set(self.pairs), set(arg.pairs))
      return engender(pairs, self.duration.written)

   ## PUBLIC ATTRIBUTES ##

   @apply
   def accidentals( ):
      def fget(self):
         raise Exception(NotImplemented)
      def fset(self, arglist):
         raise Exception(NotImplemented)
      return property(**locals( ))

   @apply
   def articulations( ):
      def fget(self):
         return self._articulations
      def fset(self, arg):
         if arg is None:
            self._articulations[ : ] = [ ]
         elif isinstance(arg, list):
            self._articulations[ : ] = arg
         else:
            raise ValueError('must be None or list of articulations.')
      return property(**locals( ))

   @apply
   def duration( ):
      def fget(self):
         return self._duration
      return property(**locals( ))

   @apply
   def dynamics( ):
      def fget(self):
         return self._dynamics
      def fset(self, arg):
         self._dynamics.mark = arg
      return property(**locals( ))

   @apply
   def glissando( ):
      def fget(self):
         return self._glissando   
      def fset(self, arg):
         if arg is None:
            self._glissando._set = False
         elif isinstance(arg, bool):
            self._glissando._set = arg 
         else:
            raise ValueError('must be boolean or None.')
      return property(**locals( ))

   @apply
   def formatter( ):
      def fget(self):
         return self._formatter
      def fset(self, arg):
         if isinstance(arg, _LeafFormatter):
            self._formatter = arg
         else:
            raise ValueError('must be _LeafFormatter.')
      return property(**locals( ))

   @apply
   def grace( ):
      def fget(self):
         return self._grace
      def fset(self, *args):
         raise ValueError('can not overwrite _GraceInterface.')
      return property(**locals( ))
   
   @apply
   def harmonic( ):
      def fget(self):
         return self._harmonic   
      def fset(self, arg):
         if arg is None:
            self._harmonic._set = False
         elif isinstance(arg, bool):
            self._harmonic._set = arg 
         else:
            raise ValueError('must be boolean or None.')
      return property(**locals( ))

   @apply
   def markup( ):
      def fget(self):
         return self._markup
      return property(**locals( ))

   @apply
   def history( ):
      def fget(self):
         return self._history
      def fset(self, *args):
         raise ValueError('history is read-only.')
      return property(**locals( ))
   
   @property
   def leaves(self):
      return [self]

   @property
   def signature(self):
      return (self.pairs, 
         (self.duration.written._n, self.duration.written._d))

   @apply
   def spanners( ):
      def fget(self):
         return self._spanners
      def fset(self, arg):
         if isinstance(arg, _LeafSpannerAggregator):
            self._spanners = arg
         else:
            raise ValueError('must be _LeafSpannerAggregator')
      return property(**locals( ))

   @apply
   def staff( ):
      def fget(self):
         return self._staff.effective
      def fset(self, arg):
         if arg is None:
            self._staff._forced = arg
         else:
            assert arg.__class__.__name__ == 'Staff'
            self._staff._forced = arg
      return property(**locals( ))

   @apply
   def tie( ):
      def fget(self):
         return self._tie
      return property(**locals( ))

   ## TODO: put behind self.navigator?
   ##       so self.navigator.next and self.navigator.prev?

   # next leaf rightwards, if any; otherwise None.
   @property
   def next(self):
      from abjad.staff.staff import Staff
      nextNode, lastVisitedRank = self._navigator._nextNodeHelper( )
      while nextNode is not None and not isinstance(nextNode, _Leaf):
         nextNode, lastVisitedRank = \
            nextNode._navigator._nextNodeHelper(lastVisitedRank)
      ## TODO fix this; it's not a staff comparison we need
      ##      but instead a 'governor' comparison ... ie,
      ##      what ever container is greatest and shows
      ##      implicit voice
      if nextNode:
         if nextNode.parentage._first(Staff) == \
            self.parentage._first(Staff):
            return nextNode
      return None

   # prev leaf leftwards, if any; otherwise None.
   @property
   def prev(self):
      from abjad.staff.staff import Staff
      prevNode, lastVisitedRank = self._navigator._prevNodeHelper( )
      while prevNode is not None and not isinstance(prevNode, _Leaf):
         prevNode, lastVisitedRank = \
            prevNode._navigator._prevNodeHelper(lastVisitedRank)
      ## TODO fix this; it's not a staff comparison we need
      ##      but instead a 'governor' comparison ... ie,
      ##      what ever container is greatest and shows
      ##      implicit voice
      if prevNode:
         if prevNode.parentage._first(Staff) == \
            self.parentage._first(Staff):
            return prevNode
      return None

   ## PUBLIC METHODS ##

   def bequeath(self, expr):
      '''Bequeath my position-in-spanners and my position-in-parent to expr.
         After bequeathal, self is an unspanned orphan.
         Return None.'''

      receipt = self.detach( )

      parent = receipt._parentage._parent
      if parent is not None:
         parent._bind_component(receipt._parentage._index, expr)

      for spanner, index in list(receipt._spanners._pairs):
         spanner.insert(index, expr)
