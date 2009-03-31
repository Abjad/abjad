from abjad.accidental.interface import _AccidentalInterface
from abjad.barline.interface import _BarLineInterface
from abjad.beam.interface import _BeamInterface
from abjad.breaks.interface import _BreaksInterface
from abjad.core.abjadcore import _Abjad
from abjad.core.comments import _Comments
from abjad.clef.interface import _ClefInterface
from abjad.dots.interface import _DotsInterface
from abjad.dynamics.interface import _DynamicsInterface
from abjad.glissando.interface import _GlissandoInterface
from abjad.meter.interface import _MeterInterface
from abjad.navigator.navigator import _Navigator
from abjad.notehead.interface import _NoteHeadInterface
from abjad.numbering.interface import _NumberingInterface
from abjad.offset.interface import _OffsetInterface
from abjad.parentage.parentage import _Parentage
from abjad.pianopedal.interface import _PianoPedalInterface
from abjad.rational.rational import Rational
from abjad.receipt.component import _ComponentReceipt
from abjad.rest.interface import _RestInterface
from abjad.slur.interface import _SlurInterface
from abjad.stem.interface import _StemInterface
from abjad.tempo.interface import _TempoInterface
from abjad.tie.interface import _TieInterface
from abjad.text.interface import _TextInterface
from abjad.tremolo.interface import _TremoloInterface
from abjad.trill.interface import _TrillInterface
from abjad.update.interface import _UpdateInterface
from abjad.voice.interface import _VoiceInterface
import copy
import types


class _Component(_Abjad):

   def __init__(self):
      self._accidental = _AccidentalInterface(self)
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
      self._name = None
      self._navigator = _Navigator(self)
      self._notehead = _NoteHeadInterface(self)
      self._parentage = _Parentage(self)
      self._pianopedal = _PianoPedalInterface(self)
      self._rest = _RestInterface(self)
      self._slur = _SlurInterface(self)
      self._stem = _StemInterface(self)
      self._tempo = _TempoInterface(self)
      self._text = _TextInterface(self)
      self._tie = _TieInterface(self)
      self._tremolo = _TremoloInterface(self)
      self._trill = _TrillInterface(self)
      self._update = _UpdateInterface(self)
      ## Observer interfaces must instantiate lexically after _UpdateInterface
      self._numbering = _NumberingInterface(self, self._update)
      self._offset = _OffsetInterface(self, self._update)
      self._voice = _VoiceInterface(self)

   ## OVERLOADS ##

   def __mul__(self, n):
      result = [ ]
      for i in range(n):
         result.append(self.copy( ))
      return result

   def __rmul__(self, n):
      return self * n

   ## PRIVATE ATTRIBUTES ##

   @property
   def _ID(self):
      if self.name is not None:
         rhs = self.name
      else:
         rhs = id(self)
      lhs = self.__class__.__name__
      return '%s-%s' % (lhs, rhs)

   ## PUBLIC ATTRIBUTES ##

   @apply
   def accidental( ):
      def fget(self):
         return self._accidental
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
      return self.formatter.format

   @property
   def formatter(self):
      return self._formatter

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
   def music(self):
      if hasattr(self, '_music'):
         return tuple(self._music)
      else:
         return tuple( )

   @apply
   def name( ):
      def fget(self):
         return self._name
      def fset(self, arg):
         assert isinstance(arg, (str, types.NoneType))
         self._name = arg
      return property(**locals( ))

   @property
   def notehead(self):
      return self._notehead

   @property
   def numbering(self):
      return self._numbering

   @property
   def offset(self):
      return self._offset

   @property
   def parentage(self):
      return self._parentage

   @property
   def pianopedal(self):
      return self._pianopedal

   @apply
   def rest( ):
      def fget(self):
         return self._rest
      return property(**locals( ))

   @apply
   def slur( ):
      def fget(self):
         return self._slur
      return property(**locals( ))

   @property
   def spanners(self):
      return self._spanners

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

   ## PUBLIC METHODS ##

   def bequeath(self, component):
      '''Give my music to recipient component.
         Give my attached spanners to recipient component.
         Give my position in parent to recipient component.
         After bequeathal, self is an empty unspanned orphan.
         Bequeath swaps out one type of container for another.
         Return None.'''
      from abjad.helpers.give_dominant_spanners_to import \
         _give_dominant_spanners_to
      from abjad.helpers.give_my_position_in_parent_to import \
         _give_my_position_in_parent_to
      from abjad.helpers.give_my_spanned_music_to import \
         _give_my_spanned_music_to
      _give_my_spanned_music_to(self, component)
      _give_dominant_spanners_to([self], [component])
      _give_my_position_in_parent_to(self, [component])

   def copy(self):
      '''Clones a complete Abjad component;
         first fractures and then cuts parent;
         (cut followed by fracture destroys 'next');
         deepcopies reference-pruned version of self;
         reestablishes parent and spanner references;
         returns the deepcopy;
         leaves self unchanged.'''

#      hairpins = self.spanners.get(classname = '_Hairpin')
#      hairpinKillList = [ ]
#      clientLeaves = set(self.leaves)
#      hairpinKillList = [
#         not set(hp[ : ]).issubset(clientLeaves) for hp in hairpins]

      #receipts = self.spanners.fracture( )
      receipts = self.spanners._fractureContents( )
      parent = self.parentage._cutOutgoingReferenceToParent( )
      result = copy.deepcopy(self)
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
      self.parentage.parent = parent

#      for i, hp in enumerate(result.spanners.get(classname = '_Hairpin')):
#         if hairpinKillList[i]:
#            hp.die( )

      result._update._markForUpdateToRoot( )
      return result

   def detach(self):
      '''Detach component from parentage.
         Detach component from spanners.
         Detach children of component from spanners.
         Return receipt.'''
      from abjad.helpers.detach_subtree import detach_subtree
      parent = self.parentage.parent
      receipt = detach_subtree(self)
      if parent is not None:
         parent._update._markForUpdateToRoot( )
      return receipt

   def reattach(self, receipt):
      '''Reattach component to both parentage in receipt.
         Reattach component to spanners in receipt.
         Empty receipt and return component.'''
      assert self is receipt._component
      self.parentage._reattach(receipt._parentage)
      self.spanners._reattach(receipt._spanners)
      receipt._empty( )
      return self

   def slip(self):
      '''Give spanners attached directly to container to children.
         Give children to parent.
         Return empty, childless container.'''
      from abjad.helpers.get_parent_and_indices import \
         get_parent_and_indices
      parent, start, stop = get_parent_and_indices([self])
      result = parent[start:stop+1] = list(self.music)
      return self
