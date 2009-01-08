from abjad.core.abjadcore import _Abjad
from abjad.barline.interface import _BarLineInterface
from abjad.beam.interface import _BeamInterface
from abjad.breaks.interface import _BreaksInterface
from abjad.clef.interface import _ClefInterface
from abjad.core.comments import _Comments
from abjad.core.parentage import _Parentage
from abjad.dots.interface import _DotsInterface
from abjad.dynamics.interface import _DynamicsInterface
from abjad.helpers.hasname import hasname
from abjad.glissando.interface import _GlissandoInterface
from abjad.meter.interface import _MeterInterface
from abjad.navigator.navigator import _Navigator
from abjad.offset.interface import _OffsetInterface
from abjad.rational.rational import Rational
from abjad.rest.interface import _RestInterface
from abjad.stem.interface import _StemInterface
from abjad.tempo.interface import _TempoInterface
from abjad.tie.interface import _TieInterface
from abjad.text.interface import _TextInterface
from abjad.tremolo.interface import _TremoloInterface
from abjad.trill.interface import _TrillInterface
from abjad.update.interface import _UpdateInterface
from abjad.voice.interface import _VoiceInterface
from copy import deepcopy


class _Component(_Abjad):

   def __init__(self):
      self._accidentals = None
      self._barline = _BarLineInterface(self)
      self._beam = _BeamInterface(self)
      self._breaks = _BreaksInterface(self)
      self._clef = _ClefInterface(self)
      self._comments = _Comments( )
      self._dots = _DotsInterface(self)
      self._dynamics = _DynamicsInterface(self)
      self._glissando = _GlissandoInterface(self)
      self._meter = _MeterInterface(self)
      self._navigator = _Navigator(self)
      self._offset = _OffsetInterface(self)
      self._parentage = _Parentage(self)
      self._rest = _RestInterface(self)
      self._stem = _StemInterface(self)
      self._tempo = _TempoInterface(self)
      self._text = _TextInterface(self)
      self._tie = _TieInterface(self)
      self._tremolo = _TremoloInterface(self)
      self._trill = _TrillInterface(self)
      self._update = _UpdateInterface(self)
      self._voice = _VoiceInterface(self)

   ### OVERLOADS ###

   def __mul__(self, n):
      result = [ ]
      for i in range(n):
         result.append(self.copy( ))
      return result

   def __rmul__(self, n):
      return self * n

   ### PUBLIC ATTRIBUTES ###

   ### TODO - make work for leaves, too    ###
   ###        add stuff to leaf formatters ###

   @apply
   def accidentals( ):
      def fget(self):
         return self._accidentals
      def fset(self, style):
         assert isinstance(style, (str, type(None)))
         self._accidentals = style
      return property(**locals( ))

   @apply
   def barline( ):
      def fget(self):
         return self._barline
      def fset(self, type):
         self._barline.type = type
      return property(**locals( ))
   
   @apply
   def beam( ):
      def fget(self):
         return self._beam
      return property(**locals( ))

   @apply
   def breaks( ):
      def fget(self):
         return self._breaks
      return property(**locals( ))

   @apply
   def clef( ):
      def fget(self):
         return self._clef
      def fset(self, arg):
         self._clef.forced = arg
      return property(**locals( ))

   @apply
   def comments( ):
      def fget(self):
         return self._comments
      def fset(self, type):
         raise AttributeError('can not overwrite _Comments.')
      return property(**locals( ))

   @apply
   def dots( ):
      def fget(self):
         return self._dots
      return property(**locals( ))

   @apply
   def dynamics( ):
      def fget(self):
         return self._dynamics
      return property(**locals( ))

   @property
   def format(self):
      return self.formatter.lily

   @apply
   def glissando( ):
      def fget(self):
         return self._glissando
      return property(**locals( ))

   @apply
   def meter( ):
      def fget(self):
         return self._meter
      def fset(self, arg):
         self._meter.forced = arg
      return property(**locals( ))

   @property
   def offset(self):
      return self._offset

   @apply
   def rest( ):
      def fget(self):
         return self._rest
      return property(**locals( ))

   @apply
   def stem( ):
      def fget(self):
         return self._stem
      return property(**locals( ))

   @apply
   def tie( ):
      def fget(self):
         return self._tie
      return property(**locals( ))

   @apply
   def tempo( ):
      def fget(self):
         return self._tempo
      def fset(self, expr):
         if expr is None:
            self._tempo._metronome = None
         elif isinstance(expr, (tuple)):
            assert isinstance(expr, tuple)
            assert isinstance(expr[0], (tuple, Rational))
            assert isinstance(expr[1], (int, float, long))
            from abjad.note.note import Note
            if isinstance(expr[0], tuple):
               self._tempo._metronome = (Note(0, expr[0]), expr[1])
            elif isinstance(expr[0], Rational):
               self._tempo._metronome = (Note(0, expr[0]), expr[1])
      return property(**locals( ))

   @apply
   def text( ):
      def fget(self):
         return self._text
      return property(**locals( ))

   @apply
   def tremolo( ):
      def fget(self):
         return self._tremolo
      return property(**locals( ))

   @apply
   def trill( ):
      def fget(self):
         return self._trill
      return property(**locals( ))

   @property
   def voice(self):
      return self._voice

   ### PUBLIC METHODS ###

   def copy(self):
      '''
      Clones a complete Abjad component;
      first fractures and then cuts parent;
      (cut followed by fracture destroys 'next');
      deepcopies reference-pruned version of self;
      reestablishes parent and spanner references;
      returns the deepcopy;
      leaves self unchanged.
      '''

#      hairpins = self.spanners.get(classname = '_Hairpin')
#      hairpinKillList = [ ]
#      clientLeaves = set(self.leaves)
#      hairpinKillList = [
#         not set(hp[ : ]).issubset(clientLeaves) for hp in hairpins]

      #receipts = self.spanners.fracture( )
      receipts = self.spanners._fractureContents( )
      parent = self._parentage._cutOutgoingReferenceToParent( )
      result = deepcopy(self)
#      for source, left, right in reversed(receipt):
#         source._unblock( )
#         left._sever( )
#         right._sever( )
      for receipt in reversed(receipts):
         if len(receipt) == 3:
            source, left, right = receipt
            center = None
         else:
            source, left, center, right = receipt
         #print 'flamingo: %s, %s, %s, %s' % (source, left, center, right)
         #source._unblock( )
         #left._sever( )
         source._unblockAllComponents( )
         left._severAllComponents( )
         if center is not None:
            #center._sever( )
            center._severAllComponents( )
         #right._sever( )
         right._severAllComponents( )
      self._parent = parent

#      for i, hp in enumerate(result.spanners.get(classname = '_Hairpin')):
#         if hairpinKillList[i]:
#            hp.die( )

      result._update._markForUpdateToRoot( )
      return result

   def kind(self, classname):
      return hasname(self, classname)
