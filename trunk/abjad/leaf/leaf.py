from abjad.component.component import _Component
from abjad.core.interface import _Interface
from abjad.interfaces.grace.interface import GraceInterface
from abjad.interfaces.harmonic.interface import HarmonicInterface
from abjad.interfaces.markup.interface import MarkupInterface
from abjad.leaf.duration import _LeafDurationInterface
from abjad.leaf.formatter import _LeafFormatter
from abjad.leaf.spanner.aggregator import _LeafSpannerAggregator
from abjad.rational import Rational
import operator


class _Leaf(_Component):

   def __init__(self, duration):
      _Component.__init__(self)
      self._duration = _LeafDurationInterface(self, duration)
      self._formatter = _LeafFormatter(self)
      self._grace = GraceInterface(self)
      self._harmonic = HarmonicInterface(self)
      self._markup = MarkupInterface(self)
      self._spanners = _LeafSpannerAggregator(self)

   ## OVERLOADS ##

   def __and__(self, arg):
      return self._operate(arg, operator.__and__)

   def __or__(self, arg):
      return self._operate(arg, operator.__or__)

   def __str__(self):
      return self._compact_representation

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
         '''Read-only reference to
         :class:`~abjad.articulations.interface.ArticulationsInterface`.
         '''
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
      '''Read-only reference to
      :class:`~abjad.grace.interface.GraceInterface`.
      '''
      return self._grace
   
   @property
   def harmonic(self):
      '''Read-only reference to
      :class:`~abjad.harmonic.interface.HarmonicInterface`.
      '''
      return self._harmonic

   @property
   def markup(self):
      '''Read-only reference to
      :class:`~abjad.markup.interface.MarkupInterface`.
      '''
      return self._markup

   @property
   def next(self):
      '''Read-only reference to next bead in thread.'''
      return self._navigator._nextBead

   @property
   def number(self):
      '''Read-only number of `self` in thread.'''
      self._numbering._makeSubjectUpdateIfNecessary( )
      return self._numbering._leaf

   @property
   def prev(self):
      '''Read-only reference to previous bead in thread.'''
      return self._navigator._prevBead

   @property
   def signature(self):
      '''Read-only signature of `self`.'''
      return (self.pairs, 
         (self.duration.written._n, self.duration.written._d))
