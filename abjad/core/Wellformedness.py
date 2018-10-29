from abjad.indicators.Clef import Clef
from abjad.indicators.StartHairpin import StartHairpin
from abjad.indicators.StartTextSpan import StartTextSpan
from abjad.indicators.StopHairpin import StopHairpin
from abjad.indicators.StopTextSpan import StopTextSpan
from abjad.instruments import Instrument
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

    ### PUBLIC PROPERTIES ###

    @property
    def allow_percussion_clef(self):
        """
        Is true when wellformedness allows percussion clef.

        Returns true, false or none.
        """
        return self._allow_percussion_clef

    ### PUBLIC METHODS ###

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
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	4 misrepresented flags
            0 /	5 missing parents
            4 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping text spanners
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
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping text spanners
            0 /	0 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	0 unterminated text spanners

        ..  container:: example

            Forbids percussion clef:

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness(allow_percussion_clef=False))
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	4 misrepresented flags
            0 /	5 missing parents
            4 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	0 overlapping text spanners
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
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            1 /	2 out of range pitches
            0 /	0 overlapping text spanners
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

    def check_overlapping_text_spanners(self, argument=None):
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
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	4 misrepresented flags
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
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	2 overlapping text spanners
            0 /	2 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	2 unterminated text spanners

        ..  container:: example

            Enchained text spanners are wellformed:

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
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	4 notes on wrong clef
            0 /	4 out of range pitches
            0 /	2 overlapping text spanners
            0 /	2 unmatched stop text spans
            0 /	0 unterminated hairpins
            0 /	2 unterminated text spanners

        Returns violators and total.
        """
        violators, total = [], 0
        def key(wrapper):
            if isinstance(wrapper.indicator, StartTextSpan):
                priority = 1
            else:
                priority = 0
            return (wrapper.start_offset, priority)
        for context in iterate(argument).components(Context):
            wrappers = context._dependent_wrappers[:]
            wrappers.sort(key=key)
            open_spanners = {}
            for wrapper in wrappers:
                if isinstance(wrapper.indicator, StartTextSpan):
                    #print(wrapper.indicator)
                    total += 1
                    command = wrapper.indicator.command
                    command = command.replace('start', '')
                    command = command.replace('Start', '')
                    #print(command, 'START', wrapper.start_offset)
                    if command not in open_spanners:
                        open_spanners[command] = []
                    if open_spanners[command]:
                        violators.append(wrapper.component)
                    open_spanners[command].append(wrapper.component)
                elif isinstance(wrapper.indicator, StopTextSpan):
                    #print(wrapper.indicator)
                    command = wrapper.indicator.command
                    command = command.replace('stop', '')
                    command = command.replace('Stop', '')
                    #print(command, 'STOP', wrapper.start_offset)
                    if command in open_spanners and open_spanners[command]:
                        open_spanners[command].pop()
        return violators, total

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
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	4 misrepresented flags
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
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	4 misrepresented flags
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
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	4 misrepresented flags
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
                if (parameter == 'DYNAMIC' or
                    isinstance(wrapper.indicator, StopHairpin)):
                    last_dynamic = wrapper.indicator
                    last_tag = wrapper.tag
                    if isinstance(wrapper.indicator, StartHairpin):
                        total += 1
            if (isinstance(last_dynamic, StartHairpin) and
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
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	4 misrepresented flags
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
