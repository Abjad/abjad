### TODO - decide whether to rename to _Leaf ###

from .. articulations.interface import ArticulationsInterface
from .. beam.interface import BeamInterface
from .. clef.clef import Clef
from .. core.component import _Component
from .. dots.interface import DotsInterface
from duration import LeafDurationInterface
from .. dynamics.interface import DynamicsInterface
from .. glissando.interface import GlissandoInterface
from .. grace.interface import GraceInterface
from .. core.interface import _Interface
from formatter import LeafFormatter
from spannerinterface import LeafSpannerInterface
from .. duration.rational import Rational
from .. staff.interface import StaffInterface
from .. stem.interface import StemInterface
from .. tremolo.interface import TremoloInterface
from .. trill.interface import TrillInterface

class Leaf(_Component):

   def __init__(self, duration):
      _Component.__init__(self)
      self._parent = None
      self._articulations = ArticulationsInterface(self)
      self.beam = BeamInterface(self)
      self.dots = DotsInterface(self)
      self._duration = LeafDurationInterface(self, duration)
      self._dynamics = DynamicsInterface(self)
      self.formatter = LeafFormatter(self)
      self._glissando = GlissandoInterface(self)
      self.grace = GraceInterface( )
      self.history = { }
      self.spanners = LeafSpannerInterface(self)
      self._staff = StaffInterface(self)
      self.stem = StemInterface(self)
      self.tremolo = TremoloInterface(self)
      self.trill = TrillInterface(self)

   ### REPR ###

   def __repr__(self):
      return self._body

   ### MANAGED ATTRIBUTES ###
   
   @apply
   def duration( ):
      def fget(self):
         return self._duration
      def fset(self, *args):
         if isinstance(args[0], (int, long)):
            rational = Rational(args[0])
         elif isinstance(args[0], tuple):
            rational = Rational(*args[0])
         elif isinstance(args[0], (Rational, Rational)):
            rational = Rational(*args[0].pair)
         else:
            raise ValueError('can not set duration from %s.' % str(args))
         self._duration.written = rational
      return property(**locals( ))

   @apply
   def glissando( ):
      def fget(self):
         return self._glissando   
      def fset(self, arg):
         if isinstance(arg, bool):
            self._glissando._set = arg 
         else:
            raise ValueError('must be boolean.')
      return property(**locals( ))

   @property
   def number(self):
      cur = self
      i = 0
      while cur.prev:
         cur = cur.prev
         i += 1
      return i

   @property
   def offset(self):
      cur = self
      offset = 0
      while cur.prev:
         cur = cur.prev
         offset += cur.duration.prolated
      return offset

   @apply
   def clef( ):
      def fget(self):
         if hasattr(self, '_clef'):
            return self._clef
         else:
            cur = self.prev
            while cur:
               if hasattr(cur, '_clef'):
                  return cur._clef
               else:
                  cur = cur.prev  
            return Clef('treble')
      def fset(self, arg):
         if arg is None:
            if hasattr(self, '_clef'):
               del self._clef
         elif isinstance(arg, str):
            self._clef = Clef(arg)
         elif isinstance(arg, Clef):
            self._clef = Clef(arg.name)
         else:
            raise ValueError('clef %s must be str or clef.' % arg)
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
   def articulations( ):
      def fget(self):
         return self._articulations
      def fset(self, arg):
         if arg is None:
            self._articulations[ : ] = [ ]
         elif isinstance(arg, (list, tuple)):
            self._articulations[ : ] = arg
         else:
            raise ValueError('must be None or list of articulations.')
      return property(**locals( ))

   @apply
   def dynamics( ):
      def fget(self):
         return self._dynamics
      def fset(self, arg):
         self._dynamics.mark = arg
      return property(**locals( ))

   ### NAVIGATION ###

   # next leaf rightwards, if any; otherwise None.
   @property
   def next(self):
      nextNode, lastVisitedRank = self._navigator._nextNodeHelper( )
      while nextNode != None and not isinstance(nextNode, Leaf):
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
      while prevNode != None and not isinstance(prevNode, Leaf):
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
      for spanner in self.spanners.get( ):
         spanner._sever(spanner.index(self))
      self._parentage._detach( )

   @property
   def leaves(self):
      return [self]
