### TODO - decide whether to rename to _Leaf ###

from .. articulations.interface import ArticulationsInterface
from .. beam.interface import BeamInterface
from .. clef.clef import Clef
from .. core.component import _Component
from .. duration.duration import Duration
from .. dynamics.interface import DynamicsInterface
from .. glissando.interface import GlissandoInterface
from .. core.history import HistoryInterface
from .. core.interface import _Interface
from formatter import LeafFormatter
from .. duration.rational import Rational
from leafspanner import LeafSpannerInterface
from .. staff.interface import StaffInterface
from .. stem.interface import StemInterface
from .. tempo.interface import TempoInterface
from .. tremolo.interface import TremoloInterface

class Leaf(_Component):

   def __init__(self, duration = None, multiplier = None):
      _Component.__init__(self)
      self._parent = None
      self._articulations = ArticulationsInterface(self)
      self.beam = BeamInterface(self)
      self._dynamics = DynamicsInterface(self)
      self.formatter = LeafFormatter(self)
      self.glissando = GlissandoInterface(self)
      self.duration = duration
      self.history = HistoryInterface(self)
      self.multiplier = multiplier
      self.spanners = LeafSpannerInterface(self)
      self._staff = StaffInterface(self)
      self.stem = StemInterface(self)
      self.tempo = TempoInterface(self)
      self.tremolo = TremoloInterface(self)

   ### REPR ###

   def __repr__(self):
      return self._body

   ### MANAGED ATTRIBUTES ###
   
   @apply
   def duration( ):
      def fget(self):
         return self._duration
      def fset(self, *args):
         if args[0] is None:
            duration = None
         elif isinstance(args[0], (int, long)):
            duration = Duration(args[0])
         elif isinstance(args[0], tuple):
            duration = Duration(*args[0])
         elif isinstance(args[0], (Duration, Rational)):
            duration = Duration(*args[0].pair)
         else:
            raise ValueError('can not set duration from %s.' % str(args))
         if duration is not None and not duration.isNoteHeadAssignable( ):
            raise ValueError('duration %s must be notehead-assignable.' % 
               duration)
         else:
            self._duration = duration
      return property(**locals( ))

   @apply
   def multiplier( ):
      def fget(self):
         return self._multiplier
      def fset(self, *args):
         if args[0] is None:
            multiplier = None
         elif isinstance(args[0], (int, long)):
            multiplier = Rational(args[0])
         elif isinstance(args[0], tuple):
            multiplier = Rational(*args[0])
         elif isinstance(args[0], (Duration, Rational)):
            multiplier = Rational(*args[0].pair)
         else:
            raise ValueError('can not set multiplier from %s.' % str(args))
         if multiplier and multiplier <= 0:
            raise ValueError('multiplier %s must be positive.' % multiplier)
         else:
            self._multiplier = multiplier
      return property(**locals( ))

   @property
   def _product(self):
      if self.duration and self.multiplier:
         return '%s * %s' % (self.duration.lily, self.multiplier)
      elif self.duration:
         return self.duration.lily
      elif self.multiplier:
         return '0 * %s' % self.multiplier
      else:
         return ''
   
   @property
   def duratum(self):
      if self.duration and self.multiplier:
         result = self._parentage._prolation * self.duration * self.multiplier
         return Duration(*result.pair)
      elif self.duration:
         result = self._parentage._prolation * self.duration
         return Duration(*result.pair)
      else:
         return None

   ### TODO - profile self.prev and optimize;                ###
   ###        this works ... but it's WAAAAY too slow to use ###

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
      offset = Duration(0)
      while cur.prev:
         cur = cur.prev
         offset += cur.duratum
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
            self._staff.forced = arg
         else:
            assert arg.__class__.__name__ == 'Staff'
            self._staff.forced = arg
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

   ### DURATION REWRITE ###

   ### TODO - decide whether to implement a DurationInterface to 
   ###        encapsulate leaf.duration, leaf.multiplier and
   ###        leaf.rewriteDurationAs( ).
   ###        Advantage: cleans up public Leaf interface;
   ###        disadvantage: makes duration accessible as
   ###        Leaf.duration.duration.
   ###        I'm leaning towards encapsulation to conform to all
   ###        the other Interfaces.

   def rewriteDurationAs(self, duration):
      if self.duration:
         previous = self.duration
         self.duration = duration
         if self.multiplier:
            multiplier = previous * self.multiplier / self.duration
         else:
            multiplier = previous / self.duration
         if multiplier != 1:
            self.multiplier = multiplier

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
         spanner.sever(spanner.index(self))
      self._parentage._detach( )

   ### TODO - extend self.instances to handle leaves ###

   @property
   def leaves(self):
      return [self]

   ### TODO - decide whether to leave Leaf.getInstances and
   ###        Container.getInstances where they are, or to 
   ###        move to Component.getInstances.
   
   def getInstances(self, name):
      result = [ ]
      if self.kind(name):
         result.append(self)
      return result
