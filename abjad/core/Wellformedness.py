import typing

from abjad import const
from abjad.indicators.Clef import Clef
from abjad.indicators.StartBeam import StartBeam
from abjad.indicators.StartHairpin import StartHairpin
from abjad.indicators.StartTextSpan import StartTextSpan
from abjad.indicators.StopBeam import StopBeam
from abjad.indicators.StopHairpin import StopHairpin
from abjad.indicators.StopTextSpan import StopTextSpan
from abjad.instruments import Instrument
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.system.Tags import Tags
from abjad.top.inspect import inspect
from abjad.top.iterate import iterate
from abjad.utilities.Duration import Duration
from abjad.utilities.Sequence import Sequence

from .Container import Container
from .Context import Context

abjad_tags = Tags()


class Wellformedness(object):
    """
    Wellformedness.

    ..  container:: example

        >>> abjad.Wellformedness()
        Wellformedness()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Collaborators"

    _publish_storage_format = True

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        """
        Calls all wellformedness checks on ``argument``.

        Returns triples.
        """
        if argument is None:
            return
        check_names = [_ for _ in dir(self) if _.startswith("check_")]
        triples = []
        for current_check_name in sorted(check_names):
            current_check = getattr(self, current_check_name)
            current_violators, current_total = current_check(argument=argument)
            triple = (current_violators, current_total, current_check_name)
            triples.append(triple)
        return triples

    def __repr__(self) -> str:
        """
        Delegates to storage format manager.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _aggregate_context_wrappers(self, argument):
        """
        Special_Voice may contain other instances of Special_Voice.
        This currently happens with OnBeatGraceContainer.
        This method aggregates all Special_Voice wrappers for checks.
        """
        name_to_wrappers: typing.Dict = {}
        for context in iterate(argument).components(Context):
            if context.name not in name_to_wrappers:
                name_to_wrappers[context.name] = []
            wrappers = context._dependent_wrappers[:]
            name_to_wrappers[context.name].extend(wrappers)
        return name_to_wrappers

    ### PUBLIC METHODS ###

    def check_beamed_long_notes(self, argument=None) -> typing.Tuple[typing.List, int]:
        r"""
        Checks beamed long notes.

        ..  container:: example

            Beamed quarter notes are not wellformed:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> abjad.attach(abjad.StartBeam(), voice[0])
            >>> abjad.attach(abjad.StopBeam(), voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    [
                    d'4
                    ]
                    e'4
                    f'4
                }

            >>> agent = abjad.inspect(voice)
            >>> print(agent.tabulate_wellformedness())
            2 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping text spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

            Beamed eighth notes are wellformed:

            >>> voice = abjad.Voice("c'8 d'8 e'8 f'8")
            >>> abjad.attach(abjad.StartBeam(), voice[0])
            >>> abjad.attach(abjad.StopBeam(), voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'8
                    [
                    d'8
                    ]
                    e'8
                    f'8
                }

            >>> agent = abjad.inspect(voice)
            >>> print(agent.tabulate_wellformedness())
            0 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping text spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

        ..  container:: example

            REGRESSION. Matching start- and stop-beam indicators work
            correctly:

            >>> voice = abjad.Voice("c'8 d'8 e'4 f'2")
            >>> abjad.attach(abjad.StartBeam(), voice[0])
            >>> abjad.attach(abjad.StopBeam(), voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'8
                    [
                    d'8
                    ]
                    e'4
                    f'2
                }

            >>> agent = abjad.inspect(voice)
            >>> print(agent.tabulate_wellformedness())
            0 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping text spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

        The examples above feature Abjad voice containers because beams are
        voice-persistent.
        """
        violators, total = [], 0
        for leaf in iterate(argument).leaves():
            total += 1
            if leaf.written_duration < Duration((1, 4)):
                continue
            start_wrapper = inspect(leaf).effective_wrapper(StartBeam)
            if start_wrapper is None:
                continue
            stop_wrapper = inspect(leaf).effective_wrapper(StopBeam)
            if stop_wrapper is None:
                violators.append(leaf)
                continue
            if stop_wrapper.leaked_start_offset < start_wrapper.leaked_start_offset:
                violators.append(leaf)
                continue
            leaf_start_offset = inspect(leaf).timespan().start_offset
            if stop_wrapper.leaked_start_offset == leaf_start_offset:
                violators.append(leaf)
        return violators, total

    def check_duplicate_ids(self, argument=None) -> typing.Tuple[typing.List, int]:
        """
        Checks duplicate IDs.
        """
        violators = []
        components = iterate(argument).components()
        total_ids = [id(_) for _ in components]
        unique_ids = Sequence(total_ids).remove_repeats()
        if len(unique_ids) < len(total_ids):
            for current_id in unique_ids:
                if 1 < total_ids.count(current_id):
                    violators.extend([_ for _ in components if id(_) == current_id])
        return violators, len(total_ids)

    def check_empty_containers(self, argument=None) -> typing.Tuple[typing.List, int]:
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

        """
        violators, containers = [], set()
        for container in iterate(argument).components(Container):
            containers.add(container)
            if len(container) == 0:
                violators.append(container)
        return violators, len(containers)

    def check_missing_parents(self, argument=None) -> typing.Tuple[typing.List, int]:
        """
        Checks missing parents.
        """
        violators, total = [], set()
        components = iterate(argument).components()
        for i, component in enumerate(components):
            total.add(component)
            if 0 < i:
                parentage = inspect(component).parentage()
                if parentage.parent is None:
                    violators.append(component)
        return violators, len(total)

    def check_notes_on_wrong_clef(
        self, argument=None
    ) -> typing.Tuple[typing.List, int]:
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
            0 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            4 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping text spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

        ..  container:: example

            Always allows percussion clef:

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
            >>> print(agent.tabulate_wellformedness())
            0 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping text spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

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
            allowable_clefs.append(Clef("percussion"))
            if clef not in allowable_clefs:
                violators.append(leaf)
        return violators, len(total)

    def check_out_of_range_pitches(
        self, argument=None
    ) -> typing.Tuple[typing.List, int]:
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
            0 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            1 /	2 out of range pitches
            0 /	0 overlapping text spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

        ..  container:: example

            Allows out-of-range pitches:

            >>> staff = abjad.Staff("c'8 r8 <d fs>8 r8")
            >>> violin = abjad.Violin()
            >>> abjad.attach(violin, staff[0])
            >>> abjad.attach(abjad.const.ALLOW_OUT_OF_RANGE, staff[2])
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
            0 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	2 out of range pitches
            0 /	0 overlapping text spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

        """
        violators, total = [], set()
        for leaf in iterate(argument).leaves(pitched=True):
            total.add(leaf)
            if inspect(leaf).has_indicator(const.ALLOW_OUT_OF_RANGE):
                continue
            if inspect(leaf).has_indicator(const.HIDDEN):
                continue
            instrument = inspect(leaf).effective(Instrument)
            if instrument is None:
                continue
            if leaf not in instrument.pitch_range:
                violators.append(leaf)
        return violators, len(total)

    def check_overlapping_text_spanners(
        self, argument=None
    ) -> typing.Tuple[typing.List, int]:
        r"""
        Checks overlapping text spanners.

        ..  container:: example

            Overlapping text spanners are not wellformed:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> abjad.text_spanner(voice)
            >>> abjad.text_spanner(voice[1:3])
            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \startTextSpan
                c'4
                \startTextSpan
                c'4
                \stopTextSpan
                c'4
                \stopTextSpan
            }

            >>> agent = abjad.inspect(voice)
            >>> print(agent.tabulate_wellformedness())
            0 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            1 /	2 overlapping text spanners
            0 /	2 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	2 unterminated text spanners

        ..  container:: example

            Overlapping text spanners with different IDs are wellformed:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> abjad.text_spanner(voice)
            >>> command = r'\startTextSpanOne'
            >>> start_text_span = abjad.StartTextSpan(command=command)
            >>> abjad.attach(start_text_span, voice[1])
            >>> command = r'\stopTextSpanOne'
            >>> stop_text_span = abjad.StopTextSpan(command=command)
            >>> abjad.attach(stop_text_span, voice[2])
            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \startTextSpan
                c'4
                \startTextSpanOne
                c'4
                \stopTextSpanOne
                c'4
                \stopTextSpan
            }

            >>> agent = abjad.inspect(voice)
            >>> print(agent.tabulate_wellformedness())
            0 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	2 overlapping text spanners
            0 /	2 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	2 unterminated text spanners

        ..  container:: example

            Enchained text spanners do not overlap (and are wellformed):

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> abjad.text_spanner(voice[:3])
            >>> abjad.text_spanner(voice[-2:])
            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \startTextSpan
                c'4
                c'4
                \stopTextSpan
                \startTextSpan
                c'4
                \stopTextSpan
            }

            >>> agent = abjad.inspect(voice)
            >>> print(agent.tabulate_wellformedness())
            0 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	2 overlapping text spanners
            0 /	2 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	2 unterminated text spanners

        ..  container:: example

            REGRESSION. Matching start- and stop-text-spans on a single leaf do
            not overlap (and are wellformed) iff stop-text-span leaks to the
            right:

            >>> voice = abjad.Voice("c'2 d'2 e'2 f'2")
            >>> abjad.attach(abjad.StartTextSpan(), voice[0])
            >>> stop_text_span = abjad.StopTextSpan(leak=True)
            >>> abjad.attach(stop_text_span, voice[0])
            >>> abjad.attach(abjad.StartTextSpan(), voice[2])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            >>> abjad.f(voice)
            \new Voice
            {
                c'2
                \startTextSpan
                <> \stopTextSpan
                d'2
                e'2
                \startTextSpan
                f'2
                \stopTextSpan
            }

            >>> agent = abjad.inspect(voice)
            >>> print(agent.tabulate_wellformedness())
            0 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	2 overlapping text spanners
            0 /	2 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	2 unterminated text spanners

        """
        violators, total = [], 0

        def key(wrapper):
            if isinstance(wrapper.indicator, StartTextSpan):
                priority = 1
            else:
                priority = 0
            return (wrapper.leaked_start_offset, priority)

        name_to_wrappers = self._aggregate_context_wrappers(argument)
        for name, wrappers in name_to_wrappers.items():
            wrappers.sort(key=key)
            open_spanners: typing.Dict = {}
            for wrapper in wrappers:
                if isinstance(wrapper.indicator, StartTextSpan):
                    total += 1
                    command = wrapper.indicator.command
                    command = command.replace("start", "")
                    command = command.replace("Start", "")
                    if command not in open_spanners:
                        open_spanners[command] = []
                    if open_spanners[command]:
                        violators.append(wrapper.component)
                    open_spanners[command].append(wrapper.component)
                elif isinstance(wrapper.indicator, StopTextSpan):
                    command = wrapper.indicator.command
                    command = command.replace("stop", "")
                    command = command.replace("Stop", "")
                    if command in open_spanners and open_spanners[command]:
                        open_spanners[command].pop()
        return violators, total

    def check_unmatched_stop_text_spans(
        self, argument=None
    ) -> typing.Tuple[typing.List, int]:
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
            0 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping text spanners
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

        """
        violators, total = [], 0
        name_to_wrappers = self._aggregate_context_wrappers(argument)
        for name, wrappers in name_to_wrappers.items():
            wrappers.sort(key=lambda _: _.leaked_start_offset)
            open_spanners: typing.Dict = {}
            for wrapper in wrappers:
                if isinstance(wrapper.indicator, StartTextSpan):
                    total += 1
                    command = wrapper.indicator.command
                    command = command.replace("start", "")
                    command = command.replace("Start", "")
                    if command not in open_spanners:
                        open_spanners[command] = []
                    open_spanners[command].append(wrapper.component)
                elif isinstance(wrapper.indicator, StopTextSpan):
                    command = wrapper.indicator.command
                    command = command.replace("stop", "")
                    command = command.replace("Stop", "")
                    if command not in open_spanners or not open_spanners[command]:
                        violators.append(wrapper.component)
                    else:
                        open_spanners[command].pop()
        return violators, total

    def check_unterminated_hairpins(
        self, argument=None
    ) -> typing.Tuple[typing.List, int]:
        r"""
        Checks unterminated hairpins.

        ..  container:: example

            Unterminated crescendo is not wellformed:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> start_hairpin = abjad.StartHairpin('<')
            >>> abjad.attach(start_hairpin, voice[0])
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
            0 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping text spanners
            0 /	0 unmatched stop text spans
            1 /	1 unterminated hairpins
            0 /	0 unterminated text spanners

            Even with start dynamic:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> dynamic = abjad.Dynamic('f')
            >>> abjad.attach(dynamic, voice[0])
            >>> start_hairpin = abjad.StartHairpin('<')
            >>> abjad.attach(start_hairpin, voice[0])
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
            0 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping text spanners
            0 /	0 unmatched stop text spans
            1 /	1 unterminated hairpins
            0 /	0 unterminated text spanners

            Terminated crescendo is wellformed:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> start_hairpin = abjad.StartHairpin('<')
            >>> abjad.attach(start_hairpin, voice[0])
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

        ..  container:: example

            Bang-terminated crescendo is wellformed:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> start_hairpin = abjad.StartHairpin('<')
            >>> abjad.attach(start_hairpin, voice[0])
            >>> stop_hairpin = abjad.StopHairpin()
            >>> abjad.attach(stop_hairpin, voice[-1])
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
                    \!
                }

            >>> abjad.inspect(voice).wellformed()
            True

        """
        violators, total = [], 0
        name_to_wrappers = self._aggregate_context_wrappers(argument)
        for name, wrappers in name_to_wrappers.items():
            last_dynamic = None
            last_tag = None
            wrappers.sort(key=lambda _: _.leaked_start_offset)
            for wrapper in wrappers:
                parameter = getattr(wrapper.indicator, "parameter", None)
                if parameter == "DYNAMIC" or isinstance(wrapper.indicator, StopHairpin):
                    last_dynamic = wrapper.indicator
                    last_tag = wrapper.tag
                    if isinstance(wrapper.indicator, StartHairpin):
                        total += 1
            if isinstance(last_dynamic, StartHairpin) and str(
                abjad_tags.RIGHT_BROKEN
            ) not in str(last_tag):
                violators.append(wrapper.component)
        return violators, total

    def check_unterminated_text_spanners(
        self, argument=None
    ) -> typing.Tuple[typing.List, int]:
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
            0 /	4 beamed long notes
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	1 overlapping text spanners
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

        """
        violators, total = [], 0
        name_to_wrappers = self._aggregate_context_wrappers(argument)
        for name, wrappers in name_to_wrappers.items():
            wrappers.sort(key=lambda _: _.leaked_start_offset)
            open_spanners: typing.Dict = {}
            for wrapper in wrappers:
                if isinstance(wrapper.indicator, StartTextSpan):
                    total += 1
                    command = wrapper.indicator.command
                    command = command.replace("start", "")
                    command = command.replace("Start", "")
                    if command not in open_spanners:
                        open_spanners[command] = []
                    open_spanners[command].append(wrapper.component)
                elif isinstance(wrapper.indicator, StopTextSpan):
                    command = wrapper.indicator.command
                    command = command.replace("stop", "")
                    command = command.replace("Stop", "")
                    if command not in open_spanners or not open_spanners[command]:
                        # unmatched stop text span
                        pass
                    else:
                        open_spanners[command].pop()
            for command, list_ in open_spanners.items():
                for component in list_:
                    violators.append(component)
        return violators, total
