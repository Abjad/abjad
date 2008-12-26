from abjad.articulations.interface import _ArticulationsInterface
from abjad.beam.interface import _BeamInterface
from abjad.clef.clef import _Clef
from abjad.clef.interface import _ClefInterface
from abjad.component.component import _Component
from abjad.core.interface import _Interface
from abjad.dots.interface import _DotsInterface
from abjad.dynamics.interface import _DynamicsInterface
from abjad.glissando.interface import _GlissandoInterface
from abjad.grace.interface import _GraceInterface
from abjad.harmonic.interface import _HarmonicInterface
from abjad.markup.interface import _MarkupInterface
from abjad.leaf.duration import _LeafDurationInterface
from abjad.leaf.formatter import _LeafFormatter
from abjad.leaf.spanner.aggregator import _LeafSpannerAggregator
from abjad.rational.rational import Rational
from abjad.staff.interface import _StaffInterface
from abjad.stem.interface import _StemInterface
from abjad.tie.interface import _TieInterface
from abjad.tremolo.interface import _TremoloInterface
from abjad.trill.interface import _TrillInterface
import operator


### TODO - take away the ability to say for x in t.spanners ...
###
###        It's now confusing to remember what t.spanners actually
###        iterates over: over spanners attaching directly to t?
###        Or over spanners attaching to the parents of t?
###
###        Better to implement some read-only lists like
###        t.spanners.mine, t.spanners.inherited, t.spanners.total.

class _Leaf(_Component):

   def __init__(self, duration):
      _Component.__init__(self)
      self._parent = None
      self._articulations = _ArticulationsInterface(self)
      self._beam = _BeamInterface(self)
      self._clef = _ClefInterface(self)
      self._dots = _DotsInterface(self)
      self._duration = _LeafDurationInterface(self, duration)
      self._dynamics = _DynamicsInterface(self)
      self._formatter = _LeafFormatter(self)
      self._glissando = _GlissandoInterface(self)
      self._grace = _GraceInterface( )
      self._harmonic = _HarmonicInterface(self)
      self._history = { }
      self._markup = _MarkupInterface(self)
      self._spanners = _LeafSpannerAggregator(self)
      self._staff = _StaffInterface(self)
      self._stem = _StemInterface(self)
      self._tie = _TieInterface(self)
      self._tremolo = _TremoloInterface(self)
      self._trill = _TrillInterface(self)

   ### OVERLOADS ###

   def __and__(self, arg):
      return self._operate(arg, operator.__and__)

   def __or__(self, arg):
      return self._operate(arg, operator.__or__)

   def __sub__(self, arg):
      return self._operate(arg, operator.__sub__)

   def __xor__(self, arg):
      return self._operate(arg, operator.__xor__)

   ### PRIVATE METHODS ###

   def _operate(self, arg, operator):
      assert isinstance(arg, _Leaf)
      from abjad.helpers.engender import engender
      pairs = operator(set(self.pairs), set(arg.pairs))
      return engender(pairs, self.duration.written.pair)

   ### PUBLIC ATTRIBUTES ###

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
   def beam( ):
      def fget(self):
         return self._beam
      def fset(self, *args):
         raise ValueError('can not overwrite _BeamInterface.')
      return property(**locals( ))
   
#   @apply
#   def clef( ):
#      def fget(self):
#         return self._clef
#      def fset(self, arg):
#         self._clef.forced = arg
#      return property(**locals( ))

#   @apply
#   def clef( ):
#      def fget(self):
#         if hasattr(self, '_clef'):
#            return self._clef
#         else:
#            cur = self.prev
#            while cur:
#               if hasattr(cur, '_clef'):
#                  return cur._clef
#               else:
#                  cur = cur.prev  
#            return _Clef('treble')
#      def fset(self, arg):
#         if arg is None:
#            if hasattr(self, '_clef'):
#               del self._clef
#         elif isinstance(arg, str):
#            self._clef = _Clef(arg)
#         elif isinstance(arg, _Clef):
#            self._clef = _Clef(arg.name)
#         else:
#            raise ValueError('clef %s must be str or clef.' % arg)
#      return property(**locals( ))

   @apply
   def dots( ):
      def fget(self):
         return self._dots
      def fset(self, *args):
         raise ValueError('can not overwrite _DotsInterface.')
      return property(**locals( ))
   
   @apply
   def duration( ):
      def fget(self):
         return self._duration
#      def fset(self, *args):
#         if isinstance(args[0], (int, long)):
#            rational = Rational(args[0])
#         elif isinstance(args[0], tuple):
#            rational = Rational(*args[0])
#         elif isinstance(args[0], (Rational, Rational)):
#            rational = Rational(*args[0].pair)
#         else:
#            raise ValueError('can not set duration from %s.' % str(args))
#         self._duration.written = rational
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
   def number(self):
      cur = self
      i = 0
      while cur.prev:
         cur = cur.prev
         i += 1
      return i

#   @property
#   def offset(self):
##      cur = self
##      offset = 0
##      while cur.prev:
##         cur = cur.prev
##         offset += cur.duration.prolated
##      return offset
#### This handles parallel structures correctly. 
#### TODO: this is still not general enough. 
#### We want to be able to offset based on thread AND non-thread.
#### We also probably want ALL components (containers too) to have an offset.
#### Make an offset interface?: _Leaf.offset.local, _Leaf.offset.global
#### [VA] Done!!! #########
#      cur = self
#      offset = 0
#      while cur._navigator._prevBead:
#         cur = cur._navigator._prevBead
#         offset += cur.duration.prolated
#      return offset

   @property
   def signature(self):
      return (self.pairs, self.duration.written.pair)

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
   def stem( ):
      def fget(self):
         return self._stem
      def fset(self, *args):
         raise ValueError('can not overwrite _StemInterface.')
      return property(**locals( ))
   
   @apply
   def tie( ):
      def fget(self):
         return self._tie
      def fset(self, arg):
         if arg is None:
            self._tie._set = False
         elif isinstance(arg, bool):
            self._tie._set = arg
         else:
            raise ValueError('must be boolean or None.')
      return property(**locals( ))

   @apply
   def tremolo( ):
      def fget(self):
         return self._tremolo
      def fset(self, *args):
         raise ValueError('can not overwrite _TremoloInterface.')
      return property(**locals( ))
   
   @apply
   def trill( ):
      def fget(self):
         return self._trill
      def fset(self, *args):
         raise ValueError('can not overwrite _TrillInterface.')
      return property(**locals( ))
   
   ### NAVIGATION ###
   ### TODO: put behind self.navigator?
   ###       so self.navigator.next and self.navigator.prev?

   # next leaf rightwards, if any; otherwise None.
   @property
   def next(self):
      nextNode, lastVisitedRank = self._navigator._nextNodeHelper( )
      while nextNode is not None and not isinstance(nextNode, _Leaf):
         nextNode, lastVisitedRank = \
            nextNode._navigator._nextNodeHelper(lastVisitedRank)
      ### TODO fix this; it's not a staff comparison we need
      ###      but instead a 'governor' comparison ... ie,
      ###      what ever container is greatest and shows
      ###      implicit voice
      if nextNode:
         #print nextNode._parentage._staff, self._parentage._staff
         #if nextNode._parentage._staff == self._parentage._staff:
         if nextNode._parentage._first('Staff') == \
            self._parentage._first('Staff'):
            return nextNode
      return None

   # prev leaf leftwards, if any; otherwise None.
   @property
   def prev(self):
      prevNode, lastVisitedRank = self._navigator._prevNodeHelper( )
      while prevNode is not None and not isinstance(prevNode, _Leaf):
         prevNode, lastVisitedRank = \
            prevNode._navigator._prevNodeHelper(lastVisitedRank)
      ### TODO fix this; it's not a staff comparison we need
      ###      but instead a 'governor' comparison ... ie,
      ###      what ever container is greatest and shows
      ###      implicit voice
      if prevNode:
         #print prevNode._parentage._staff, self._parentage._staff
         #if prevNode._parentage._staff == self._parentage._staff:
         if prevNode._parentage._first('Staff') == \
            self._parentage._first('Staff'):
            return prevNode
      return None

   ### TODO - encapsulate somewhere ###

   def _die(self):
      #for spanner in self.spanners.get( ):
      for spanner in self.spanners.attached:
         #spanner._sever(spanner.index(self))
         spanner.remove(self)
      self._parentage._detach( )
