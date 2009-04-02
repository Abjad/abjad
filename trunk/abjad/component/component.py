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
from abjad.instrument.interface import _InstrumentInterface
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
from abjad.tuplet.bracket import _TupletBracketInterface
from abjad.tuplet.number import _TupletNumberInterface
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
      self._instrument = _InstrumentInterface(self)
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
      self._tupletbracket = _TupletBracketInterface(self)
      self._tupletnumber = _TupletNumberInterface(self)
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

   @property
   def instrument(self):
      return self._instrument

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
   def tupletbracket(self):
      return self._tupletbracket

   @property
   def tupletnumber(self):
      return self._tupletnumber

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
      receipts = self.spanners._fractureContents( )
      parent = self.parentage._cutOutgoingReferenceToParent( )
      result = copy.deepcopy(self)
      for receipt in reversed(receipts):
         if len(receipt) == 3:
            source, left, right = receipt
            center = None
         else:
            source, left, center, right = receipt
         source._unblockAllComponents( )
         left._severAllComponents( )
         if center is not None:
            center._severAllComponents( )
         right._severAllComponents( )
      self.parentage.parent = parent
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

   def splice(self, components):
      '''Splice 'components' after self.
         Extend spanners to attached to all components in list.'''
      from abjad.helpers.assert_components import assert_components
      from abjad.helpers.get_dominant_spanners import get_dominant_spanners
      from abjad.helpers.get_parent_and_indices import get_parent_and_indices
      from abjad.helpers.spanner_get_component_at_score_offset import \
         spanner_get_component_at_score_offset
      assert_components(components)
      insert_offset = self.offset.score + self.duration.prolated
      receipt = get_dominant_spanners([self])
      for spanner, index in receipt:
         insert_component = spanner_get_component_at_score_offset(
            spanner, insert_offset)
         if insert_component is not None:
            insert_index = spanner.index(insert_component)
         else:
            insert_index = len(spanner)
         for component in reversed(components):
            spanner._insert(insert_index, component)
            component.spanners._add(spanner)
      parent, start, stop = get_parent_and_indices([self])
      if parent is not None:
         for component in reversed(components):
            component.parentage._switchParentTo(parent)
            parent._music.insert(start + 1, component)
      return [self] + components

   def splice_left(self, components):
      '''Splice 'components' before self.
         Extend spanners leftwards to attach 
         to all components in 'components'.'''
      from abjad.helpers.assert_components import assert_components
      from abjad.helpers.get_dominant_spanners import get_dominant_spanners
      from abjad.helpers.get_parent_and_indices import get_parent_and_indices
      from abjad.helpers.spanner_get_index_at_score_offset import \
         spanner_get_index_at_score_offset
      assert_components(components)
      offset = self.offset.score
      receipt = get_dominant_spanners([self])
      for spanner, x in receipt:
         index = spanner_get_index_at_score_offset(spanner, offset)
         for component in reversed(components):
            spanner._insert(index, component)
            component.spanners._add(spanner)
      parent, start, stop = get_parent_and_indices([self])
      if parent is not None:
         for component in reversed(components):
            component.parentage._switchParentTo(parent)
            parent._music.insert(start, component)
      return components + [self] 
