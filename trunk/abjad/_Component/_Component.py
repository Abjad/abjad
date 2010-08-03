from abjad.core.abjadcore import _Abjad
from abjad.interfaces import _UpdateInterface
from abjad.interfaces import AccidentalInterface
from abjad.interfaces import ArticulationInterface
from abjad.interfaces import BarLineInterface
from abjad.interfaces import BarNumberInterface
from abjad.interfaces import BeamInterface
from abjad.interfaces import BreaksInterface
from abjad.interfaces import CommentsInterface
from abjad.interfaces import ClefInterface
from abjad.interfaces import DirectivesInterface
from abjad.interfaces import DotsInterface
from abjad.interfaces import DynamicsInterface
from abjad.interfaces import DynamicLineSpannerInterface
from abjad.interfaces import DynamicTextInterface
from abjad.interfaces import DynamicTextSpannerInterface
from abjad.interfaces import GlissandoInterface
from abjad.interfaces import HairpinInterface
from abjad.interfaces import HistoryInterface
from abjad.interfaces import InstrumentInterface
from abjad.interfaces import InterfaceAggregator
from abjad.interfaces import KeySignatureInterface
from abjad.interfaces import MeterInterface
from abjad.interfaces import MultiMeasureRestInterface
from abjad.interfaces import NonMusicalPaperColumnInterface
from abjad.interfaces import NoteColumnInterface
from abjad.interfaces import NoteHeadInterface
from abjad.interfaces import NumberingInterface
from abjad.interfaces import OffsetInterface
from abjad.interfaces import OttavaBracketInterface
from abjad.interfaces import ParentageInterface
from abjad.interfaces import PianoPedalInterface
from abjad.interfaces import RehearsalMarkInterface
from abjad.interfaces import RestInterface
from abjad.interfaces import ScoreInterface
from abjad.interfaces import ScriptInterface
from abjad.interfaces import SlurInterface
from abjad.interfaces import SpacingInterface
from abjad.interfaces import SpanBarInterface
from abjad.interfaces import StaffInterface
from abjad.interfaces import StemInterface
from abjad.interfaces import StemTremoloInterface
from abjad.interfaces import SystemStartBarInterface
from abjad.interfaces import TempoInterface
from abjad.interfaces import TextScriptInterface
from abjad.interfaces import TextSpannerInterface
from abjad.interfaces import ThreadInterface
from abjad.interfaces import TieInterface
from abjad.interfaces import TremoloInterface
from abjad.interfaces import TrillInterface
from abjad.interfaces import TrillPitchAccidentalInterface
from abjad.interfaces import TupletBracketInterface
from abjad.interfaces import TupletNumberInterface
from abjad.interfaces import VerticalAlignmentInterface
from abjad.interfaces import VerticalAxisGroupInterface
from abjad.interfaces import VoiceInterface
from abjad._Navigator._Navigator import _Navigator
from abjad.Rational import Rational
import copy
import types


class _Component(_Abjad):

## TODO?: could __slots__ improve Abjad's performance?
#   __slots__ = ('_interfaces', '_accidental', '_articulations', '_bar_line', 
#      '_bar_number', '_beam', '_breaks', '_comments', '_directives', 
#      '_dots', '_dynamics', '_dynamic_line_spanner', '_dynamic_text', 
#      '_dynamic_text_spanner', '_glissando', '_hairpin', '_history', 
#      '_instrument', '_lily_file', '_name', '_navigator', 
#      '_non_musical_paper_column', '_note_column', '_note_head', 
#      '_ottava_bracket', '_parentage', '_piano_pedal', '_rehearsal_mark', 
#      '_rest', '_score', '_script', '_slur', '_spacing', '_span_bar', '_stem', 
#      '_stem_tremolo', '_system_start_bar', '_text_script', '_text_spanner', 
#      '_thread', '_tie', '_tremolo', '_trill', '_trill_pitch_accidental', 
#      '_tuplet_bracket', '_tuplet_number', '_update', '_verical_alignment', 
#      '_vertical_axis_group')

   def __init__(self):
      self._interfaces = InterfaceAggregator(self)
      self._accidental = AccidentalInterface(self)
      self._articulations = ArticulationInterface(self)
      self._bar_line = BarLineInterface(self)
      self._bar_number = BarNumberInterface(self)
      self._beam = BeamInterface(self)
      self._breaks = BreaksInterface(self)
      self._comments = CommentsInterface( )
      self._directives = DirectivesInterface(self)
      self._dots = DotsInterface(self)
      self._dynamics = DynamicsInterface(self)
      self._dynamic_line_spanner = DynamicLineSpannerInterface(self)
      self._dynamic_text = DynamicTextInterface(self)
      self._dynamic_text_spanner = DynamicTextSpannerInterface(self)
      self._glissando = GlissandoInterface(self)
      self._hairpin = HairpinInterface(self)
      self._history = HistoryInterface(self)
      self._instrument = InstrumentInterface(self)
      self._lily_file = None
      self._multi_measure_rest = MultiMeasureRestInterface(self)
      self._name = None
      self._navigator = _Navigator(self)
      self._non_musical_paper_column = NonMusicalPaperColumnInterface(self)
      self._note_column = NoteColumnInterface(self)
      self._note_head = NoteHeadInterface(self)
      self._ottava_bracket = OttavaBracketInterface(self)
      self._parentage = ParentageInterface(self)
      self._piano_pedal = PianoPedalInterface(self)
      self._rehearsal_mark = RehearsalMarkInterface(self)
      self._rest = RestInterface(self)
      self._score = ScoreInterface(self)
      self._script = ScriptInterface(self)
      self._slur = SlurInterface(self)
      self._spacing = SpacingInterface(self)
      self._span_bar = SpanBarInterface(self)
      self._stem = StemInterface(self)
      self._stem_tremolo = StemTremoloInterface(self)
      self._system_start_bar = SystemStartBarInterface(self)
      self._text_script = TextScriptInterface(self)
      self._text_spanner = TextSpannerInterface(self)
      self._thread = ThreadInterface(self)
      self._tie = TieInterface(self)
      self._tremolo = TremoloInterface(self)
      self._trill = TrillInterface(self)
      self._trill_pitch_accidental = TrillPitchAccidentalInterface(self)
      self._tuplet_bracket = TupletBracketInterface(self)
      self._tuplet_number = TupletNumberInterface(self)
      self._update = _UpdateInterface(self)
      self._vertical_alignment = VerticalAlignmentInterface(self)
      self._vertical_axis_group = VerticalAxisGroupInterface(self)

      ## Observer Interfaces must instantiate after _UpdateInterface ##
      self._clef = ClefInterface(self, self._update)
      self._key_signature = KeySignatureInterface(self, self._update)
      self._meter = MeterInterface(self, self._update)
      self._numbering = NumberingInterface(self, self._update)
      self._offset = OffsetInterface(self, self._update)
      self._staff = StaffInterface(self, self._update)
      self._tempo = TempoInterface(self, self._update)
      self._voice = VoiceInterface(self)

   ## OVERLOADS ##

   def __mul__(self, n):
      from abjad.tools import componenttools
      return componenttools.clone_components_and_remove_all_spanners([self], n)

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
      :class:`~abjad.interfaces.accidental.interface.AccidentalInterface`.'''
      return self._accidental

   @property
   def articulations(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.articulation.interface.ArticulationInterface`.'''
      return self._articulations
   
   @property
   def bar_line(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.bar_line.interface.BarLineInterface`.'''
      return self._bar_line

   @property
   def bar_number(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.bar_number.interface.BarNumberInterface`.'''
      return self._bar_number
   
   @property
   def beam(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.beam.interface.BeamInterface`.'''
      return self._beam

   @property
   def breaks(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.breaks.interface.BreaksInterface`.'''
      return self._breaks

   @property
   def clef(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.clef.interface.ClefInterface`.'''
      return self._clef

   @property
   def comments(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.comments.interface.CommentsInterface`.'''
      return self._comments

   @property
   def directives(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.directives.interface.DirectivesInterface`.'''
      return self._directives

   @property
   def dots(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.dots.interface.DotsInterface`.'''
      return self._dots

   @property
   def duration(self):
      '''Read-only reference to class-specific duration interface.'''
      return self._duration

   @property
   def dynamic_line_spanner(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.dynamic_line_spanner.interface.DynamicLineSpannerInterface`.'''
      return self._dynamic_line_spanner

   @property
   def dynamic_text(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.dynamic_text.interface.DynamicTextInterface`.'''
      return self._dynamic_text

   @property
   def dynamic_text_spanner(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.dynamic_text_spanner.interface.DynamicTextSpannerInterface`.'''
      return self._dynamic_text_spanner

   @property
   def dynamics(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.dynamics.interface.DynamicsInterface`.'''
      return self._dynamics

   @property
   def format(self):
      '''Read-only version of `self` as LilyPond input code.'''
      return self._formatter.format

   @property
   def glissando(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.glissando.interface.GlissandoInterface`.'''
      return self._glissando

   @property
   def hairpin(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.hairpin.interface.HairpinInterface`.'''
      return self._hairpin

   @property
   def history(self):
      '''Read-only reference to 
      :class:`~abjad.interfaces.history.interface.HistoryInterface`.'''
      return self._history

   @property
   def instrument(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.instrument.interface.InstrumentInterface`.'''
      return self._instrument

   @property
   def interfaces(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.interface_aggregator.aggregator.InterfaceAggregator`.'''
      return self._interfaces

   @property
   def key_signature(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.key_signature.interface.KeySignatureInterface.`
      '''
      return self._key_signature

   @property
   def leaves(self):
      '''Read-only tuple of all leaves in `self`.

      .. versionchanged:: 1.1.1'''
      from abjad.tools import iterate
      return tuple(iterate.leaves_forward_in_expr(self))

   @property
   def lily_file(self):
      '''.. versionadded:: 1.1.2
      Read-only reference to .ly file in which 
      component is housed, if any.'''
      return self._lily_file

   ## TODO: rename to time_siganture ##
   @property
   def meter(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.meter.interface.MeterInterface`.''' 
      return self._meter

   @property
   def multi_measure_rest(self):
      '''Read-only reference to
      :clas:`~abjad.interfaces.multi_measure_rest.interface.MultiMeasureRestInterface`.'''
      return self._multi_measure_rest

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
         '''Read-write name of component. Must be string or none.'''
         return self._name
      def fset(self, arg):
         assert isinstance(arg, (str, types.NoneType))
         self._name = arg
      return property(**locals( ))

   @property
   def non_musical_paper_column(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.non_musical_paper_column.interface.NonMusicalPaperColumnInterface`.
      '''
      return self._non_musical_paper_column

   @property
   def note_column(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.note_column.interface.NoteColumnInterface`.'''
      return self._note_column

   @property
   def note_head(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.note_head.interface.NoteHeadInterface`.'''
      return self._note_head

   @property
   def offset(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.offset.interface.OffsetInterface`.'''
      return self._offset

   @property
   def ottava_bracket(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.ottava_bracket.interface.OttavaBracketInterface`.'''
      return self._ottava_bracket

   @property
   def parentage(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.parentage.interface.ParentageInterface`.'''
      return self._parentage

   @property
   def piano_pedal(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.piano_pedal.interface.PianoPedalInterface`.'''
      return self._piano_pedal

   @property
   def rehearsal_mark(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.rehearsal_mark.interface.RestInterface`.'''
      return self._rehearsal_mark

   @property
   def rest(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.rest.interface.RestInterface`.'''
      return self._rest

   @property
   def score(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.score.interface.ScoreInterface`.'''
      return self._score

   @property
   def script(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.script.interface.ScriptInterface`.'''
      return self._script

   @property
   def slur(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.slur.interface.SlurInterface`.'''
      return self._slur

   @property
   def spacing(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.spacing.interface.SpacingInterface`.'''
      return self._spacing

   @property
   def span_bar(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.span_bar.interface.SpanBarInterface`.'''
      return self._span_bar

   @property
   def spanners(self):
      '''Read-only reference to
      :class:`~abjad._Component.spanner.aggregator._ComponentSpannerAggregator`.

      .. todo:: move to abjad/interfaces/spanner_aggregator directory.
      '''
      return self._spanners
   
   @property
   def staff(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.staff.interface.StaffInterface`.'''
      return self._staff

   @property
   def stem(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.stem.interface.StemInterface`.'''
      return self._stem

   @property
   def stem_tremolo(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.stem_tremolo.interface.StemTremoloInterface`.'''
      return self._stem_tremolo

   @property
   def system_start_bar(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.system_start_bar.interface.SystemStartBarInterface`.'''
      return self._system_start_bar

   @property
   def thread(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.thread.interface.ThreadInterface`.'''
      return self._thread

   @property
   def tie(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.tie.interface.TieInterface`.'''
      return self._tie

   ## TODO: rename to metronome_mark ##
   @property
   def tempo(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.tempo.interface.TempoInterface`.'''
      return self._tempo

   @property
   def text_script(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.text_script.interface.TextScriptInterface`.
      '''
      return self._text_script

   @property
   def text_spanner(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.text_spanner.interface.TextSpannerInterface`.'''
      return self._text_spanner

   @property
   def tremolo(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.tremolo.interface.TremoloInterface`.'''
      return self._tremolo

   @property
   def trill(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.trill.interface.TrillInterface`.'''
      return self._trill
   
   @property
   def trill_pitch_accidental(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.trill_pitch_accidental.interface.TrillPitchAccidentalInterface`.'''
      return self._trill_pitch_accidental
   
   @property
   def tuplet_bracket(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.tuplet_bracket.interface.TupletBracketInterface`.'''
      return self._tuplet_bracket

   @property
   def tuplet_number(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.tuplet_number.interface.TupletNumberInterface`.'''
      return self._tuplet_number

   @property
   def vertical_alignment(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.vertical_alignment.interface.VerticalAlignmentInterface`.'''
      return self._vertical_alignment

   @property
   def vertical_axis_group(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.vertical_axis_group.interface.VerticalAxisGroupInterface`.'''
      return self._vertical_axis_group

   @property
   def voice(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.voice.interface.VoiceInterface`.'''
      return self._voice

   ## PUBLIC METHODS ##

   def extend_in_parent(self, components):
      r'''.. versionadded:: 1.1.1

      Extend `components` rightwards of `self` in parent.

      Do not extend edge spanners. ::

         abjad> t = Voice(macros.scale(3))
         abjad> Beam(t[:])
         abjad> t[-1].extend_in_parent(macros.scale(3))

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

      from abjad.tools import componenttools
      from abjad.tools import parenttools
      assert componenttools.all_are_components(components)
      parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([self])
      if parent is not None:
         after = stop + 1
         parent[after:after] = components
      return [self] + components

   def extend_left_in_parent(self, components):
      r'''.. versionadded:: 1.1.1

      Extend `components` leftwards of `self` in parent.

      Do not extend edge spanners. ::

         abjad> t = Voice(macros.scale(3))
         abjad> Beam(t[:])
         abjad> t[0].extend_in_parent(macros.scale(3))

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

      from abjad.tools import componenttools
      from abjad.tools import parenttools
      assert componenttools.all_are_components(components)
      parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([self])
      if parent is not None:
         parent[start:start] = components
      return components + [self] 

   def splice(self, components):
      '''Splice `components` after `self`.
      Extend spanners rightwards to attach to all components in list.'''
      from abjad.tools import componenttools
      from abjad.tools import parenttools
      from abjad.tools import spannertools
      assert componenttools.all_are_components(components)
      insert_offset = self.offset.prolated.stop
      receipt = spannertools.get_spanners_that_dominate_components([self])
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
      parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([self])
      if parent is not None:
         for component in reversed(components):
            component.parentage._switch(parent)
            parent._music.insert(start + 1, component)
      return [self] + components

   def splice_left(self, components):
      '''Splice `components` before `self`.
      Extend spanners leftwards to attach to all components in list.'''
      from abjad.tools import componenttools
      from abjad.tools import parenttools
      from abjad.tools import spannertools
      assert componenttools.all_are_components(components)
      offset = self.offset.prolated.start
      receipt = spannertools.get_spanners_that_dominate_components([self])
      for spanner, x in receipt:
         index = spannertools.find_index_at_score_offset(spanner, offset)
         for component in reversed(components):
            spanner._insert(index, component)
            component.spanners._add(spanner)
      parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([self])
      if parent is not None:
         for component in reversed(components):
            component.parentage._switch(parent)
            parent._music.insert(start, component)
      return components + [self] 
