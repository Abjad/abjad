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
from abjad.rational.rational import Rational
from abjad.staff.interface import _StaffInterface
import operator


class _Leaf(_Component):

   def __init__(self, duration):
      _Component.__init__(self)
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
   def articulations( ):
      def fget(self):
         return self._articulations
      def fset(self, arg):
         if arg is None:
            self._articulations[:] = [ ]
         elif isinstance(arg, list):
            self._articulations[:] = arg
         else:
            raise ValueError('must be None or list of articulations.')
      return property(**locals( ))

#   @property
#   def duration(self):
#      return self._duration

   @property
   def grace(self):
      return self._grace
   
   @property
   def harmonic(self):
      return self._harmonic

   @property
   def markup(self):
      return self._markup

   @property
   def history(self):
      return self._history
   
   @property
   def next(self):
      return self._navigator._nextBead

   @property
   def prev(self):
      return self._navigator._prevBead

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

   @property
   def tie(self):
      return self._tie
