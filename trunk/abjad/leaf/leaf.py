from abjad.articulations.interface import _ArticulationsInterface
from abjad.component.component import _Component
from abjad.core.interface import _Interface
from abjad.grace.interface import _GraceInterface
from abjad.harmonic.interface import _HarmonicInterface
from abjad.leaf.duration import _LeafDurationInterface
from abjad.leaf.formatter import _LeafFormatter
from abjad.leaf.spanner.aggregator import _LeafSpannerAggregator
from abjad.markup.interface import _MarkupInterface
from abjad.rational.rational import Rational
from abjad.staff.interface.interface import _StaffInterface
import operator


class _Leaf(_Component):

   def __init__(self, duration):
      _Component.__init__(self)
      self._articulations = _ArticulationsInterface(self)
      self._duration = _LeafDurationInterface(self, duration)
      self._formatter = _LeafFormatter(self)
      self._grace = _GraceInterface(self)
      self._harmonic = _HarmonicInterface(self)
      self._markup = _MarkupInterface(self)
      self._spanners = _LeafSpannerAggregator(self)
      self._staff = _StaffInterface(self, self._update)

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
      from abjad.tools import construct
      pairs = operator(set(self.pairs), set(arg.pairs))
      return construct.engender(pairs, self.duration.written)

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
   def next(self):
      return self._navigator._nextBead

   @property
   def number(self):
      self._numbering._makeSubjectUpdateIfNecessary( )
      return self._numbering._leaf

   @property
   def prev(self):
      return self._navigator._prevBead

   @property
   def signature(self):
      return (self.pairs, 
         (self.duration.written._n, self.duration.written._d))

   @property
   def staff(self):
      return self._staff
