from abjad.indicators.Clef import Clef
from abjad.indicators.HairpinIndicator import HairpinIndicator
from abjad.indicators.StartTextSpan import StartTextSpan
from abjad.indicators.StopTextSpan import StopTextSpan
from abjad.instruments import Instrument
from abjad.spanners.Glissando import Glissando
from abjad.spanners.OctavationSpanner import OctavationSpanner
from abjad.spanners.Tie import Tie
from abjad.spanners.TrillSpanner import TrillSpanner
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.top.inspect import inspect
from abjad.top.iterate import iterate
from abjad.top.setting import setting
from abjad.utilities.Sequence import Sequence
from .Container import Container
from .Context import Context


class Wellformedness(object):
    """
    Wellformedness.

    ..  container:: example

        >>> abjad.Wellformedness()
        Wellformedness()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Collaborators'

    __slots__ = (
        '_allow_percussion_clef',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, allow_percussion_clef=None):
        self._allow_percussion_clef = allow_percussion_clef

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        """
        Calls all wellformedness checks on ``argument``.

        Returns triples.
        """
        if argument is None:
            return
        check_names = [_ for _ in dir(self) if _.startswith('check_')]
        triples = []
        for current_check_name in sorted(check_names):
            current_check = getattr(self, current_check_name)
            current_violators, current_total = current_check(argument=argument)
            triple = (current_violators, current_total, current_check_name)
            triples.append(triple)
        return triples

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _check_overlapping_spanners(self, argument, prototype=None):
        violators, spanners = set(), set()
        for leaf in iterate(argument).leaves():
            spanners_ = list(inspect(leaf).spanners(prototype))
            spanners.update(spanners_)
            if 1 < len(spanners_):
                if len(spanners_) == 2:
                    common_leaves = set(spanners_[0].leaves)
                    common_leaves &= set(spanners_[1].leaves)
                    if len(common_leaves) == 1:
                        leaf = list(common_leaves)[0]
                        if ((spanners_[0].leaves[0] is leaf and
                            spanners_[1].leaves[-1] is leaf) or
                            (spanners_[1].leaves[0] is leaf and
                            spanners_[0].leaves[-1] is leaf)):
                            break
                violators.update(spanners_)
        return violators, len(spanners)

    ### PUBLIC PROPERTIES ###

    @property
    def allow_percussion_clef(self):
        """
        Is true when wellformedness allows percussion clef.

        Returns true, false or none.
        """
        return self._allow_percussion_clef

    ### PUBLIC METHODS ###

    def check_discontiguous_spanners(self, argument=None):
        """
        Checks discontiguous spanners.

        There are now two different types of spanner. Most spanners demand that
        spanner components be logical-voice-contiguous. But a few special
        spanners (like MetronomeMark) do not make such a demand. The check here
        consults the experimental `_contiguity_constraint`.

        Returns list of discontiguous spanners and nonnegative integer count of
        all spanners in ``argument``.
        """
        violators = []
        descendants = inspect(argument).descendants()
        spanners = inspect(descendants).spanners()
        for spanner in spanners:
            if spanner._contiguity_constraint == 'logical voice':
                if not spanner[:].are_contiguous_logical_voice():
                    violators.append(spanner)
        return violators, len(spanners)

    def check_duplicate_ids(self, argument=None):
        """
        Checks duplicate IDs.

        Returns violators and total.
        """
        violators = []
        components = iterate(argument).components()
        total_ids = [id(_) for _ in components]
        unique_ids = Sequence(total_ids).remove_repeats()
        if len(unique_ids) < len(total_ids):
            for current_id in unique_ids:
                if 1 < total_ids.count(current_id):
                    violators.extend([_ for _ in components
                        if id(_) == current_id])
        return violators, len(total_ids)

    def check_empty_containers(self, argument=None):
        r"""
        Checks empty containers.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> staff.append(abjad.Container())

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                {
                }
            }

            >>> wellformedness = abjad.Wellformedness()
            >>> violators, total = wellformedness.check_empty_containers(staff)
            >>> violators
            [Container()]

        Returns list of empty containers and count of all containers in
        ``argument``.
        """
        violators, containers = [], set()
        for container in iterate(argument).components(Container):
            containers.add(container)
            if len(container) == 0:
                violators.append(container)
        return violators, len(containers)

    def check_mispitched_ties(self, argument=None):
        r"""
        Checks mispitched notes.

        ..  container:: example

            Checks for mispitched ties attached to notes:

            >>> staff = abjad.Staff("c'4 ~ c'")
            >>> staff[1].written_pitch = abjad.NamedPitch("d'")

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness())
            0 /	1 discontiguous spanners
            0 /	3 duplicate ids
            0 /	1 empty containers
            1 /	1 mispitched ties
            0 /	2 misrepresented flags
            0 /	3 missing parents
            0 /	2 notes on wrong clef
            0 /	2 out of range pitches
            0 /	0 overlapping glissandi
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping trill spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

        ..  container:: example

            Checks for mispitched ties attached to chords:

            >>> staff = abjad.Staff("<c' d' bf'>4 ~ <c' d' bf'>")
            >>> staff[1].written_pitches = [6, 9]

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness())
            0 /	1 discontiguous spanners
            0 /	3 duplicate ids
            0 /	1 empty containers
            1 /	1 mispitched ties
            0 /	2 misrepresented flags
            0 /	3 missing parents
            0 /	2 notes on wrong clef
            0 /	2 out of range pitches
            0 /	0 overlapping glissandi
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping trill spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

        Returns violator ties together with total number of ties.
        """
        violators, ties = [], set()
        for leaf in iterate(argument).leaves(pitched=True):
            ties_ = inspect(leaf).spanners(Tie)
            ties.update(ties_)
        for tie in ties:
            for first_leaf, second_leaf in Sequence(tie).nwise():
                first_pitches = inspect(first_leaf).pitches()
                first_pitches = set([_.number for _ in first_pitches])
                second_pitches = inspect(second_leaf).pitches()
                second_pitches = set([_.number for _ in second_pitches])
                if not (first_pitches & second_pitches):
                    violators.append(tie)
                    break
        return violators, len(ties)

    def check_misrepresented_flags(self, argument=None):
        """
        Checks misrepresented flags.

        Returns violators and total.
        """
        violators, total = [], set()
        for leaf in iterate(argument).leaves():
            total.add(leaf)
            flags = leaf.written_duration.flag_count
            left = getattr(setting(leaf), 'stem_left_beam_count', None)
            right = getattr(setting(leaf), 'stem_right_beam_count', None)
            if left is not None:
                if (flags < left or
                    (left < flags and right not in (flags, None))):
                    if leaf not in violators:
                        violators.append(leaf)
            if right is not None:
                if (flags < right or
                    (right < flags and left not in (flags, None))):
                    if leaf not in violators:
                        violators.append(leaf)
        return violators, len(total)

    def check_missing_parents(self, argument=None):
        """
        Checks missing parents.

        Returns violators and total.
        """
        violators, total = [], set()
        components = iterate(argument).components()
        for i, component in enumerate(components):
            total.add(component)
            if 0 < i:
                parentage = inspect(component).parentage(grace_notes=True)
                if parentage.parent is None:
                    violators.append(component)
        return violators, len(total)

    def check_notes_on_wrong_clef(self, argument=None):
        r"""
        Checks notes and chords on wrong clef.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> clef = abjad.Clef('alto')
            >>> abjad.attach(clef, staff[0])
            >>> violin = abjad.Violin()
            >>> abjad.attach(violin, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'8
                    d'8
                    e'8
                    f'8
                }

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness())
            0 /	0 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            4 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping glissandi
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping trill spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

        ..  container:: example

            Allows percussion clef:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> clef = abjad.Clef('percussion')
            >>> abjad.attach(clef, staff[0])
            >>> violin = abjad.Violin()
            >>> abjad.attach(violin, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "percussion"
                    c'8
                    d'8
                    e'8
                    f'8
                }

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness(allow_percussion_clef=True))
            0 /	0 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping glissandi
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping trill spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

        ..  container:: example

            Forbids percussion clef:

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness(allow_percussion_clef=False))
            0 /	0 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            4 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping glissandi
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping trill spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

        Returns true or false.
        """
        violators, total = [], set()
        for leaf in iterate(argument).leaves():
            total.add(leaf)
            instrument = inspect(leaf).effective(Instrument)
            if instrument is None:
                continue
            clef = inspect(leaf).effective(Clef)
            if clef is None:
                continue
            allowable_clefs = [Clef(_) for _ in instrument.allowable_clefs]
            if self.allow_percussion_clef:
                allowable_clefs.append(Clef('percussion'))
            if clef not in allowable_clefs:
                violators.append(leaf)
        return violators, len(total)

    def check_out_of_range_pitches(self, argument=None):
        r"""
        Checks out-of-range notes.

        ..  container:: example

            Out of range:

            >>> staff = abjad.Staff("c'8 r8 <d fs>8 r8")
            >>> violin = abjad.Violin()
            >>> abjad.attach(violin, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    r8
                    <d fs>8
                    r8
                }

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness())
            0 /	0 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            1 /	2 out of range pitches
            0 /	0 overlapping glissandi
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping trill spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

        Returns true or false.
        """
        violators, total = [], set()
        for leaf in iterate(argument).leaves(pitched=True):
            total.add(leaf)
            if inspect(leaf).annotation('HIDDEN') is True:
                continue
            instrument = inspect(leaf).effective(Instrument)
            if instrument is None:
                continue
            if leaf not in instrument.pitch_range:
                violators.append(leaf)
        return violators, len(total)

    def check_overlapping_glissandi(self, argument=None):
        """
        Checks overlapping glissandi.

        Returns violators and total.
        """
        return self._check_overlapping_spanners(argument, Glissando)

    def check_overlapping_octavation_spanners(self, argument=None):
        """
        Checks overlapping octavation spanners.

        Returns violators and total.
        """
        violators, total = [], set()
        prototype = OctavationSpanner
        for leaf in iterate(argument).leaves():
            spanners = inspect(leaf).spanners(prototype)
            total.update(spanners)
            if 1 < len(spanners):
                for spanner in spanners:
                    if spanner not in violators:
                        violators.append(spanner)
        return violators, len(total)

    def check_overlapping_trill_spanners(self, argument=None):
        r"""
        Checks overlapping trill spanners.

        ..  container:: example

            Enchained trill spanners are ok:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.TrillSpanner(), staff[:3])
            >>> abjad.attach(abjad.TrillSpanner(), staff[2:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \startTrillSpan
                    d'4
                    e'4
                    \stopTrillSpan
                    \startTrillSpan
                    f'4
                    \stopTrillSpan
                }

            >>> abjad.inspect(staff).wellformed()
            True

        ..  container:: example

            Overlapping trill spanners are not wellformed:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.TrillSpanner(), staff[:])
            >>> abjad.attach(abjad.TrillSpanner(), staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \startTrillSpan
                    \startTrillSpan
                    d'4
                    e'4
                    f'4
                    \stopTrillSpan
                    \stopTrillSpan
                }

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness())
            0 /	2 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping glissandi
            0 /	0 overlapping octavation spanners
            2 /	2 overlapping trill spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

        Enchained hairpins are fine so long as hairpin ends match.

        Returns violators and total.
        """
        return self._check_overlapping_spanners(argument, TrillSpanner)

    def check_unmatched_stop_text_spans(self, argument=None):
        r"""
        Checks unmatched stop text spans.

        ..  container:: example

            Unmatched stop text span is not wellformed:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, voice[-1])
            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                c'4
                c'4
                c'4
                \stopTextSpan
            }

            >>> agent = abjad.inspect(voice)
            >>> print(agent.tabulate_wellformedness())
            0 /	0 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping glissandi
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping trill spanners
            1 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

            Matched stop text span is wellformed:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> start_text_span = abjad.StartTextSpan()
            >>> abjad.attach(start_text_span, voice[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, voice[-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \startTextSpan
                    c'4
                    c'4
                    c'4
                    \stopTextSpan
                }

            >>> abjad.inspect(voice).wellformed()
            True

        Returns violators and total.
        """
        violators, total = [], 0
        for context in iterate(argument).components(Context):
            wrappers = context._dependent_wrappers[:]
            wrappers.sort(key=lambda _: _.start_offset)
            open_spanners = {}
            for wrapper in wrappers:
                if isinstance(wrapper.indicator, StartTextSpan):
                    total += 1
                    command = wrapper.indicator.command
                    command = command.replace('start', '')
                    command = command.replace('Start', '')
                    if command not in open_spanners:
                        open_spanners[command] = []
                    open_spanners[command].append(wrapper.component)
                elif isinstance(wrapper.indicator, StopTextSpan):
                    command = wrapper.indicator.command
                    command = command.replace('stop', '')
                    command = command.replace('Stop', '')
                    if (command not in open_spanners or
                        not open_spanners[command]):
                        violators.append(wrapper.component)
                    else:
                        open_spanners[command].pop()
        return violators, total

    def check_unterminated_hairpins(self, argument=None):
        r"""
        Checks unterminated hairpins.

        ..  container:: example

            Unterminated crescendo is not wellformed:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> hairpin = abjad.HairpinIndicator('<')
            >>> abjad.attach(hairpin, voice[0])
            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \<
                c'4
                c'4
                c'4
            }

            >>> agent = abjad.inspect(voice)
            >>> print(agent.tabulate_wellformedness())
            0 /	0 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping glissandi
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping trill spanners
            0 /	0 unmatched stop text spans
            1 /	1 unterminated hairpins
            0 /	0 unterminated text spanners

            Even with start dynamic:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> dynamic = abjad.Dynamic('f')
            >>> abjad.attach(dynamic, voice[0])
            >>> hairpin = abjad.HairpinIndicator('<')
            >>> abjad.attach(hairpin, voice[0])
            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \f
                \<
                c'4
                c'4
                c'4
            }

            >>> agent = abjad.inspect(voice)
            >>> print(agent.tabulate_wellformedness())
            0 /	0 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping glissandi
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping trill spanners
            0 /	0 unmatched stop text spans
            1 /	1 unterminated hairpins
            0 /	0 unterminated text spanners

            Terminated crescendo is wellformed:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> hairpin = abjad.HairpinIndicator('<')
            >>> abjad.attach(hairpin, voice[0])
            >>> dynamic = abjad.Dynamic('f')
            >>> abjad.attach(dynamic, voice[-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \<
                    c'4
                    c'4
                    c'4
                    \f
                }

            >>> abjad.inspect(voice).wellformed()
            True

        Returns violators and total.
        """
        violators, total = [], 0
        for context in iterate(argument).components(Context):
            last_dynamic = None
            last_tag = None
            wrappers = context._dependent_wrappers[:]
            wrappers.sort(key=lambda _: _.start_offset)
            for wrapper in wrappers:
                parameter = getattr(wrapper.indicator, 'parameter', None)
                if parameter == 'DYNAMIC':
                    last_dynamic = wrapper.indicator
                    last_tag = wrapper.tag
                    if isinstance(wrapper.indicator, HairpinIndicator):
                        total += 1
            if (isinstance(last_dynamic, HairpinIndicator) and
                'right_broken' not in str(last_tag)):
                violators.append(wrapper.component)
        return violators, total

    def check_unterminated_text_spanners(self, argument=None):
        r"""
        Checks unterminated text spanners.

        ..  container:: example

            Unterminated text spanner is not wellformed:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> start_text_span = abjad.StartTextSpan()
            >>> abjad.attach(start_text_span, voice[0])
            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \startTextSpan
                c'4
                c'4
                c'4
            }

            >>> agent = abjad.inspect(voice)
            >>> print(agent.tabulate_wellformedness())
            0 /	0 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping glissandi
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping trill spanners
            0 /	1 unmatched stop text spans
            0 /	0 unterminated hairpins
            1 /	1 unterminated text spanners

            Terminated text span is wellformed:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> start_text_span = abjad.StartTextSpan()
            >>> abjad.attach(start_text_span, voice[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, voice[-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \startTextSpan
                    c'4
                    c'4
                    c'4
                    \stopTextSpan
                }

            >>> abjad.inspect(voice).wellformed()
            True

        Returns violators and total.
        """
        violators, total = [], 0
        for context in iterate(argument).components(Context):
            wrappers = context._dependent_wrappers[:]
            wrappers.sort(key=lambda _: _.start_offset)
            open_spanners = {}
            for wrapper in wrappers:
                if isinstance(wrapper.indicator, StartTextSpan):
                    total += 1
                    command = wrapper.indicator.command
                    command = command.replace('start', '')
                    command = command.replace('Start', '')
                    if command not in open_spanners:
                        open_spanners[command] = []
                    open_spanners[command].append(wrapper.component)
                elif isinstance(wrapper.indicator, StopTextSpan):
                    command = wrapper.indicator.command
                    command = command.replace('stop', '')
                    command = command.replace('Stop', '')
                    if (command not in open_spanners or
                        not open_spanners[command]):
                        # unmatched stop text span
                        pass
                    else:
                        open_spanners[command].pop()
            for command, list_ in open_spanners.items():
                for component in list_:
                    violators.append(component)
        return violators, total
