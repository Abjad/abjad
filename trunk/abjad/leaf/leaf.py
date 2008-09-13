from .. articulations.interface import _ArticulationsInterface
from .. beam.interface import _BeamInterface
from .. clef.clef import _Clef
from .. core.component import _Component
from .. core.interface import _Interface
from .. dots.interface import _DotsInterface
from duration import _LeafDurationInterface
from .. duration.rational import Rational
from .. dynamics.interface import _DynamicsInterface
from formatter import _LeafFormatter
from .. glissando.interface import _GlissandoInterface
from .. grace.interface import _GraceInterface
from .. harmonic.interface import _HarmonicInterface
from spannerinterface import _LeafSpannerInterface
from .. staff.interface import _StaffInterface
from .. stem.interface import _StemInterface
from .. tie.interface import _TieInterface
from .. tremolo.interface import _TremoloInterface
from .. trill.interface import _TrillInterface

class _Leaf(_Component):

   def __init__(self, duration):
      _Component.__init__(self)
      self._parent = None
      self._articulations = _ArticulationsInterface(self)
      #self.beam = _BeamInterface(self)
      self._beam = _BeamInterface(self)
      #self.dots = _DotsInterface(self)
      self._dots = _DotsInterface(self)
      self._duration = _LeafDurationInterface(self, duration)
      self._dynamics = _DynamicsInterface(self)
      # TODO: can't make formatter a read-only property
      # because of casting between notes and chords;
      # come up with solution for read-only formatter
      self.formatter = _LeafFormatter(self)
      self._glissando = _GlissandoInterface(self)
      #self.grace = _GraceInterface( )
      self._grace = _GraceInterface( )
      self._harmonic = _HarmonicInterface(self)
      self.history = { }
      # TODO: can't make spanners a read-only property
      # because of /helpers/attributes.py;
      # come up with solution for read-only spanners
      self.spanners = _LeafSpannerInterface(self)
      self._staff = _StaffInterface(self)
      #self.stem = _StemInterface(self)
      self._stem = _StemInterface(self)
      self._tie = _TieInterface(self)
      #self.tremolo = _TremoloInterface(self)
      self._tremolo = _TremoloInterface(self)
      #self.trill = _TrillInterface(self)
      self._trill = _TrillInterface(self)

   ### REPR ###

   def __repr__(self):
      return self._body

   ### MANAGED ATTRIBUTES ###

   @apply
   def beam( ):
      def fget(self):
         return self._beam
      def fset(self, *args):
         raise ValueError('can not overwrite _BeamInterface.')
      return property(**locals( ))
   
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
         if arg is None:
            self._glissando._set = False
         elif isinstance(arg, bool):
            self._glissando._set = arg 
         else:
            raise ValueError('must be boolean or None.')
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
            return _Clef('treble')
      def fset(self, arg):
         if arg is None:
            if hasattr(self, '_clef'):
               del self._clef
         elif isinstance(arg, str):
            self._clef = _Clef(arg)
         elif isinstance(arg, _Clef):
            self._clef = _Clef(arg.name)
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
         elif isinstance(arg, list):
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
      for spanner in self.spanners.get( ):
         spanner._sever(spanner.index(self))
      self._parentage._detach( )

#   def _flamingo(self):
#      parent = self._parent
#      self._die( )
#      #while parent is not None:
         

   @property
   def leaves(self):
      return [self]
