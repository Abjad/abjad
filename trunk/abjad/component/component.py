from abjad.core.abjadcore import _Abjad
from abjad.interfaces.accidental.interface import AccidentalInterface
from abjad.interfaces.articulation.interface import ArticulationInterface
from abjad.interfaces.barline.interface import BarLineInterface
from abjad.interfaces.barnumber.interface import BarNumberInterface
from abjad.interfaces.beam.interface import BeamInterface
from abjad.interfaces.breaks.interface import BreaksInterface
from abjad.interfaces.comments.interface import CommentsInterface
from abjad.interfaces.clef.interface import ClefInterface
from abjad.interfaces.directives.interface import DirectivesInterface
from abjad.interfaces.dots.interface import DotsInterface
from abjad.interfaces.dynamics.interface import DynamicsInterface
from abjad.interfaces.glissando.interface import GlissandoInterface
from abjad.interfaces.history.interface import HistoryInterface
from abjad.interfaces.instrument.interface import InstrumentInterface
from abjad.interfaces.interface_aggregator.aggregator import \
   InterfaceAggregator
from abjad.interfaces.meter.interface import MeterInterface
from abjad.interfaces.nonmusicalpapercolumn.interface import \
   NonMusicalPaperColumnInterface
from abjad.interfaces.notecolumn.interface import NoteColumnInterface
from abjad.interfaces.notehead.interface import NoteHeadInterface
from abjad.interfaces.numbering.interface import NumberingInterface
from abjad.interfaces.offset.interface import OffsetInterface
from abjad.interfaces.parentage.interface import ParentageInterface
from abjad.interfaces.pianopedal.interface import PianoPedalInterface
from abjad.interfaces.rest.interface import RestInterface
from abjad.interfaces.score.interface import ScoreInterface
from abjad.interfaces.slur.interface import SlurInterface
from abjad.interfaces.spacing.interface import SpacingInterface
from abjad.interfaces.spanbar.interface import SpanBarInterface
from abjad.interfaces.staff.interface import StaffInterface
from abjad.interfaces.stem.interface import StemInterface
from abjad.interfaces.tempo.interface import TempoInterface
from abjad.interfaces.text.interface import TextInterface
from abjad.interfaces.textspanner.interface import TextSpannerInterface
from abjad.interfaces.thread.interface import ThreadInterface
from abjad.interfaces.tie.interface import TieInterface
from abjad.interfaces.tremolo.interface import TremoloInterface
from abjad.interfaces.trill.interface import TrillInterface
from abjad.interfaces.tupletbracket.interface import TupletBracketInterface
from abjad.interfaces.tupletnumber.interface import TupletNumberInterface
from abjad.interfaces.update.interface import _UpdateInterface
from abjad.interfaces.voice.interface import VoiceInterface
from abjad.navigator.navigator import _Navigator
from abjad.rational import Rational
import copy
import types


class _Component(_Abjad):

   def __init__(self):
      self._interfaces = InterfaceAggregator(self)
      self._accidental = AccidentalInterface(self)
      self._articulations = ArticulationInterface(self)
      self._barline = BarLineInterface(self)
      self._barnumber = BarNumberInterface(self)
      self._beam = BeamInterface(self)
      self._breaks = BreaksInterface(self)
      self._comments = CommentsInterface( )
      self._directives = DirectivesInterface(self)
      self._dots = DotsInterface(self)
      self._dynamics = DynamicsInterface(self)
      self._glissando = GlissandoInterface(self)
      self._history = HistoryInterface(self)
      self._instrument = InstrumentInterface(self)
      self._lily_file = None
      self._name = None
      self._navigator = _Navigator(self)
      self._nonmusicalpapercolumn = NonMusicalPaperColumnInterface(self)
      self._notecolumn = NoteColumnInterface(self)
      self._notehead = NoteHeadInterface(self)
      self._parentage = ParentageInterface(self)
      self._pianopedal = PianoPedalInterface(self)
      self._rest = RestInterface(self)
      self._score = ScoreInterface(self)
      self._slur = SlurInterface(self)
      self._spacing = SpacingInterface(self)
      self._spanbar = SpanBarInterface(self)
      self._stem = StemInterface(self)
      self._text = TextInterface(self)
      self._text_spanner = TextSpannerInterface(self)
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
   def _format_pieces(self):
      return self._formatter._format_pieces
   
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
      :class:`~abjad.articulations.interface.ArticulationInterface`.'''
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
      :class:`~abjad.comments.interface.CommentsInterface`.'''
      return self._comments

   @property
   def directives(self):
      '''Read-only reference to
      :class:`~abjad.directives.interface.DirectivesInterface`.'''
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
      return self._formatter.format

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
      return tuple(iterate.naive_forward(self, _Leaf))

   @property
   def lily_file(self):
      '''.. versionadded:: 1.1.2
      Read-only reference to .ly file in which 
      component is housed, if any.'''
      return self._lily_file

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
   def nonmusicalpapercolumn(self):
      '''Read-only reference to
      :class:`~abjad.nonmusicalpapercolumn.interface.NonMusicalPaperColumn`.
      '''
      return self._nonmusicalpapercolumn

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
      :class:`~abjad.parentage.interface.ParentageInterface`.'''
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
   def text_spanner(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.textspanner.interface.TextSpannerInterface`.'''
      return self._text_spanner

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
