from abjad.accidental.interface import AccidentalInterface
from abjad.articulations.interface import ArticulationsInterface
from abjad.barline.interface import BarLineInterface
from abjad.barnumber.interface import BarNumberInterface
from abjad.beam.interface import BeamInterface
from abjad.breaks.interface import BreaksInterface
from abjad.comments.comments import UserCommentsInterface
from abjad.core.abjadcore import _Abjad
from abjad.clef.interface import ClefInterface
from abjad.directives.interface import UserDirectivesInterface
from abjad.dots.interface import DotsInterface
from abjad.dynamics.interface import DynamicsInterface
from abjad.glissando.interface import GlissandoInterface
from abjad.history.interface import HistoryInterface
from abjad.instrument.interface import InstrumentInterface
from abjad.interfaces.aggregator import InterfaceAggregator
from abjad.meter.interface import MeterInterface
from abjad.navigator.navigator import _Navigator
from abjad.notecolumn.interface import NoteColumnInterface
from abjad.numbering.interface import NumberingInterface
from abjad.offset.interface import OffsetInterface
from abjad.parentage.parentage import Parentage
from abjad.pianopedal.interface import PianoPedalInterface
from abjad.rational import Rational
from abjad.receipt.component import _ComponentReceipt
from abjad.slur.interface import SlurInterface
from abjad.spacing.interface import SpacingInterface
from abjad.spanbar.interface import SpanBarInterface
from abjad.stem.interface import StemInterface
from abjad.tempo.interface import TempoInterface
from abjad.thread.interface import ThreadInterface
from abjad.tie.interface import TieInterface
from abjad.text.interface import TextInterface
from abjad.tremolo.interface import TremoloInterface
from abjad.trill.interface import TrillInterface
from abjad.update.interface import _UpdateInterface
import copy
import types


class _Component(_Abjad):

   def __init__(self):
      '''Late import of RestInterface, ScoreInterface, StaffInterface
      and VoiceInterface to avoid circular imports in which instantiating
      a rest imports abjad/leaf (because Rest is a _Leaf), which imports 
      abjad/component (because _Leaf is a _Component), which imports 
      abjad/rest (because _Component has a RestInterface).
   
      The solution given here with the late imports of what we might
      collectively term the 'component information interfaces' does indeed
      work but also suggests a cleaner way of laying out the codebase
      in which ALL interfaces of whatever sort, not just the component
      information interfaces imported here, collectively live inside
      some abjad/allinterfaces package.'''
      from abjad.notehead.interface import NoteHeadInterface
      from abjad.rest.interface import RestInterface
      from abjad.score.interface.interface import ScoreInterface
      from abjad.staff.interface.interface import StaffInterface
      from abjad.tuplet.bracket import TupletBracketInterface
      from abjad.tuplet.number import TupletNumberInterface
      from abjad.voice.interface.interface import VoiceInterface
      self._interfaces = InterfaceAggregator(self)
      self._accidental = AccidentalInterface(self)
      self._articulations = ArticulationsInterface(self)
      self._barline = BarLineInterface(self)
      self._barnumber = BarNumberInterface(self)
      self._beam = BeamInterface(self)
      self._breaks = BreaksInterface(self)
      self._comments = UserCommentsInterface( )
      self._directives = UserDirectivesInterface(self)
      self._dots = DotsInterface(self)
      self._dynamics = DynamicsInterface(self)
      self._glissando = GlissandoInterface(self)
      #self._history = { }
      self._history = HistoryInterface(self)
      self._instrument = InstrumentInterface(self)
      self._name = None
      self._navigator = _Navigator(self)
      self._notecolumn = NoteColumnInterface(self)
      self._notehead = NoteHeadInterface(self)
      self._parentage = Parentage(self)
      self._pianopedal = PianoPedalInterface(self)
      self._rest = RestInterface(self)
      self._score = ScoreInterface(self)
      self._slur = SlurInterface(self)
      self._spacing = SpacingInterface(self)
      self._spanbar = SpanBarInterface(self)
      self._stem = StemInterface(self)
      self._text = TextInterface(self)
      self._thread = ThreadInterface(self)
      self._tie = TieInterface(self)
      self._tremolo = TremoloInterface(self)
      self._trill = TrillInterface(self)
      self._tupletbracket = TupletBracketInterface(self)
      self._tupletnumber = TupletNumberInterface(self)
      self._update = _UpdateInterface(self)

      ## Observer Interfaces must instantiate after _UpdateInterface ##
      self._clef = ClefInterface(self, self._update)
      self._meter = MeterInterface(self, self._update)
      self._numbering = NumberingInterface(self, self._update)
      self._offset = OffsetInterface(self, self._update)
      self._staff = StaffInterface(self, self._update)
      self._tempo = TempoInterface(self, self._update)
      self._voice = VoiceInterface(self)

   ## OVERLOADS ##

   def __mul__(self, n):
      from abjad.tools import clone
      return clone.unspan([self], n)

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

   @property
   def accidental(self):
      '''Read-only reference to 
      :class:`~abjad.accidental.interface.AccidentalInterface`.'''
      return self._accidental

   @property
   def articulations(self):
      '''Read-only reference to
      :class:`~abjad.articulations.interface.ArticulationsInterface`.'''
      return self._articulations
   
   @property
   def barline(self):
      '''Read-only reference to
      :class:`~abjad.barline.interface.BarLineInterface`.'''
      return self._barline

   @property
   def barnumber(self):
      '''Read-only reference to
      :class:`~abjad.barnumber.interface.BarNumberInterface`.'''
      return self._barnumber
   
   @property
   def beam(self):
      '''Read-only reference to
      :class:`~abjad.beam.interface.BeamInterface`.'''
      return self._beam

   @property
   def breaks(self):
      '''Read-only reference to
      :class:`~abjad.breaks.interface.BreaksInterface`.'''
      return self._breaks

   @property
   def clef(self):
      '''Read-only reference to
      :class:`~abjad.clef.interface.ClefInterface`.'''
      return self._clef

   @property
   def comments(self):
      '''Read-only reference to
      :class:`~abjad.comments.comments.UserCommentsInterface`.'''
      return self._comments

   @property
   def directives(self):
      '''Read-only reference to
      :class:`~abjad.directives.interface.UserDirectivesInterface`.'''
      return self._directives

   @property
   def dots(self):
      '''Read-only reference to
      :class:`~abjad.dots.interface.DotsInterface`.'''
      return self._dots

   @property
   def duration(self):
      '''Read-only reference to class-specific duration interface.'''
      return self._duration

   @property
   def dynamics(self):
      '''Read-only reference to
      :class:`~abjad.dynamics.interface.DynamicsInterface`.'''
      return self._dynamics

   @property
   def format(self):
      '''Read-only version of `self` as LilyPond input code.'''
      return self.formatter.format

   @property
   def formatter(self):
      '''Read-only reference to class-specific formatter.'''
      return self._formatter

   @property
   def glissando(self):
      '''Read-only reference to
      :class:`~abjad.glissando.interface.GlissandoInterface`.'''
      return self._glissando

   @property
   def history(self):
      '''Read-only reference to 
      :class:`~abjad.history.interface.HistoryInterface`.'''
      return self._history

   @property
   def instrument(self):
      '''Read-only reference to
      :class:`~abjad.instrument.interface.InstrumentInterface`.'''
      return self._instrument

   @property
   def interfaces(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.aggregator.InterfaceAggregator`.'''
      return self._interfaces

   @property
   def leaves(self):
      '''Read-only tuple of all leaves in `self`.

      .. versionchanged:: 1.1.1'''
      from abjad.leaf.leaf import _Leaf
      from abjad.tools import iterate
      return tuple(iterate.naive(self, _Leaf))

   @property
   def meter(self):
      '''Read-only reference to
      :class:`~abjad.meter.interface.MeterInterface`.''' 
      return self._meter

   @property
   def music(self):
      '''Read-only tuple of music in `self`.'''
      if hasattr(self, '_music'):
         return tuple(self._music)
      else:
         return tuple( )

   @apply
   def name( ):
      def fget(self):
         '''Read-write name of `self`. Must be string or ``None``.'''
         return self._name
      def fset(self, arg):
         assert isinstance(arg, (str, types.NoneType))
         self._name = arg
      return property(**locals( ))

   @property
   def notecolumn(self):
      '''Read-only reference to
      :class:`~abjad.notecolumn.interface.NoteColumnInterface`.'''
      return self._notecolumn

   @property
   def notehead(self):
      '''Read-only reference to
      :class:`~abjad.notehead.interface.NoteHeadInterface`.'''
      return self._notehead

   @property
   def offset(self):
      '''Read-only reference to
      :class:`~abjad.offset.interface.OffsetInterface`.'''
      return self._offset

   @property
   def parentage(self):
      '''Read-only reference to
      :class:`~abjad.parentage.parentage.Parentage`.'''
      return self._parentage

   @property
   def pianopedal(self):
      '''Read-only reference to
      :class:`~abjad.pianopedal.interface.PianoPedalInterface`.'''
      return self._pianopedal

   @property
   def rest(self):
      '''Read-only reference to
      :class:`~abjad.rest.interface.RestInterface`.'''
      return self._rest

   @property
   def score(self):
      '''Read-only reference to
      :class:`~abjad.score.interface.interface.ScoreInterface`.'''
      return self._score

   @property
   def slur(self):
      '''Read-only reference to
      :class:`~abjad.slur.interface.SlurInterface`.'''
      return self._slur

   @property
   def spacing(self):
      '''Read-only reference to
      :class:`~abjad.spacing.interface.SpacingInterface`.'''
      return self._spacing

   @property
   def spanbar(self):
      '''Read-only reference to
      :class:`~abjad.spanbar.interface.SpanBarInterface`.'''
      return self._spanbar

   @property
   def spanners(self):
      '''Read-only reference to
      :class:`~abjad.component.spanner.aggregator._ComponentSpannerAggregator`.
      '''
      return self._spanners
   
   @property
   def staff(self):
      '''Read-only reference to
      :class:`~abjad.staff.interface.interface.StaffInterface`.'''
      return self._staff

   @property
   def stem(self):
      '''Read-only reference to
      :class:`~abjad.stem.interface.StemInterface`.'''
      return self._stem

   @property
   def thread(self):
      '''Read-only reference to
      :class:`~abjad.thread.interface.ThreadInterface`.'''
      return self._thread

   @property
   def tie(self):
      '''Read-only reference to
      :class:`~abjad.tie.interface.TieInterface`.'''
      return self._tie

   @property
   def tempo(self):
      '''Read-only reference to
      :class:`~abjad.tempo.interface.TempoInterface`.'''
      return self._tempo

   @property
   def text(self):
      '''Read-only reference to
      :class:`~abjad.text.interface.TextInterface`.'''
      return self._text

   @property
   def tremolo(self):
      '''Read-only reference to
      :class:`~abjad.tremolo.interface.TremoloInterface`.'''
      return self._tremolo

   @property
   def trill(self):
      '''Read-only reference to
      :class:`~abjad.trill.interface.TrillInterface`.'''
      return self._trill
   
   @property
   def tupletbracket(self):
      '''Read-only reference to
      :class:`~abjad.tuplet.bracket.TupletBracketInterface`.'''
      return self._tupletbracket

   @property
   def tupletnumber(self):
      '''Read-only reference to
      :class:`~abjad.tuplet.number.TupletNumberInterface`.'''
      return self._tupletnumber

   @property
   def voice(self):
      '''Read-only reference to
      :class:`~abjad.voice.interface.interface.VoiceInterface`.'''
      return self._voice

   ## PUBLIC METHODS ##

   def extend_in_parent(self, components):
      r'''.. versionadded:: 1.1.1

      Extend `components` rightwards of `self` in parent.

      Do not extend edge spanners. ::

         abjad> t = Voice(construct.scale(3))
         abjad> Beam(t[:])
         abjad> t[-1].extend_in_parent(construct.scale(3))

      ::

         abjad> print t.format
         \new Voice {
            c'8 [
            d'8
            e'8 ]
            c'8
            d'8
            e'8
         }
      '''

      from abjad.tools import check
      from abjad.tools import parenttools
      check.assert_components(components)
      parent, start, stop = parenttools.get_with_indices([self])
      if parent is not None:
         after = stop + 1
         parent[after:after] = components
      return [self] + components

   def extend_left_in_parent(self, components):
      r'''.. versionadded:: 1.1.1

      Extend `components` leftwards of `self` in parent.

      Do not extend edge spanners. ::

         abjad> t = Voice(construct.scale(3))
         abjad> Beam(t[:])
         abjad> t[0].extend_in_parent(construct.scale(3))

      ::

         abjad> print t.format
         \new Voice {
            c'8 
            d'8
            e'8 
            c'8 [
            d'8
            e'8 ]
         }
      '''

      from abjad.tools import check
      from abjad.tools import parenttools
      check.assert_components(components)
      parent, start, stop = parenttools.get_with_indices([self])
      if parent is not None:
         parent[start:start] = components
      return components + [self] 

   def splice(self, components):
      '''Splice `components` after `self`.
      Extend spanners rightwards to attach to all components in list.'''
      from abjad.tools import check
      from abjad.tools import parenttools
      from abjad.tools import spannertools
      check.assert_components(components)
      insert_offset = self.offset.prolated.stop
      receipt = spannertools.get_dominant([self])
      for spanner, index in receipt:
         insert_component = spannertools.find_component_at_score_offset(
            spanner, insert_offset)
         if insert_component is not None:
            insert_index = spanner.index(insert_component)
         else:
            insert_index = len(spanner)
         for component in reversed(components):
            spanner._insert(insert_index, component)
            component.spanners._add(spanner)
      parent, start, stop = parenttools.get_with_indices([self])
      if parent is not None:
         for component in reversed(components):
            component.parentage._switch(parent)
            parent._music.insert(start + 1, component)
      return [self] + components

   def splice_left(self, components):
      '''Splice `components` before `self`.
      Extend spanners leftwards to attach to all components in list.'''
      from abjad.tools import check
      from abjad.tools import parenttools
      from abjad.tools import spannertools
      check.assert_components(components)
      offset = self.offset.prolated.start
      receipt = spannertools.get_dominant([self])
      for spanner, x in receipt:
         index = spannertools.find_index_at_score_offset(spanner, offset)
         for component in reversed(components):
            spanner._insert(index, component)
            component.spanners._add(spanner)
      parent, start, stop = parenttools.get_with_indices([self])
      if parent is not None:
         for component in reversed(components):
            component.parentage._switch(parent)
            parent._music.insert(start, component)
      return components + [self] 
