import enum
import typing

from . import duration as _duration
from . import get as _get
from . import indicators as _indicators
from . import instruments as _instruments
from . import iterate as _iterate
from . import iterpitches as _iterpitches
from . import parentage as _parentage
from . import score as _score
from . import sequence as _sequence
from . import tag as _tag


def _aggregate_context_wrappers(argument):
    """
    Special_Voice may contain other instances of Special_Voice.
    This currently happens with OnBeatGraceContainer.
    This method aggregates all Special_Voice wrappers for checks.
    """
    context_name_to_wrappers = {}
    for context in _iterate.components(argument, _score.Context):
        if context.name not in context_name_to_wrappers:
            context_name_to_wrappers[context.name] = []
        wrappers = context._dependent_wrappers[:]
        context_name_to_wrappers[context.name].extend(wrappers)
    return context_name_to_wrappers


def check_beamed_lone_notes(argument) -> tuple[list, int]:
    r"""
    Checks beamed lone notes.

    ..  container:: example

        Beamed single notes are not wellformed:

        >>> voice = abjad.Voice("c'8 d' e' f'")
        >>> abjad.attach(abjad.StartBeam(), voice[0])
        >>> abjad.attach(abjad.StopBeam(), voice[0])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'8
                [
                ]
                d'8
                e'8
                f'8
            }

        >>> abjad.wf.check_beamed_lone_notes(voice)
        ([Note("c'8")], 4)

    The examples above feature Abjad voice containers because beams are
    voice-persistent.
    """
    violators, total = [], 0
    for leaf in _iterate.leaves(argument):
        total += 1
        if _get.has_indicator(leaf, _indicators.StartBeam):
            if _get.has_indicator(leaf, _indicators.StopBeam):
                violators.append(leaf)
    return violators, total


def check_beamed_long_notes(argument) -> tuple[list, int]:
    r"""
    Checks beamed long notes.

    ..  container:: example

        Beamed quarter notes are not wellformed:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> abjad.attach(abjad.StartBeam(), voice[0])
        >>> abjad.attach(abjad.StopBeam(), voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                [
                d'4
                ]
                e'4
                f'4
            }

        >>> abjad.wf.check_beamed_long_notes(voice)
        ([Note("c'4"), Note("d'4")], 4)

        Beamed eighth notes are wellformed:

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8")
        >>> abjad.attach(abjad.StartBeam(), voice[0])
        >>> abjad.attach(abjad.StopBeam(), voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'8
                [
                d'8
                ]
                e'8
                f'8
            }

        >>> abjad.wf.check_beamed_long_notes(voice)
        ([], 4)

    The examples above feature Abjad voice containers because beams are
    voice-persistent.
    """
    violators, total = [], 0
    for leaf in _iterate.leaves(argument):
        total += 1
        if leaf.written_duration < _duration.Duration((1, 4)):
            continue
        start_wrapper = _get.effective(leaf, _indicators.StartBeam, unwrap=False)
        if start_wrapper is None:
            continue
        stop_wrapper = _get.effective(leaf, _indicators.StopBeam, unwrap=False)
        if stop_wrapper is None:
            violators.append(leaf)
            continue
        if stop_wrapper.leaked_start_offset < start_wrapper.leaked_start_offset:
            violators.append(leaf)
            continue
        leaf_start_offset = leaf._get_timespan().start_offset
        if stop_wrapper.leaked_start_offset == leaf_start_offset:
            violators.append(leaf)
    return violators, total


def check_duplicate_ids(argument) -> tuple[list, int]:
    """
    Checks duplicate IDs.
    """
    violators = []
    components = _iterate.components(argument)
    total_ids = [id(_) for _ in components]
    unique_ids = _sequence.remove_repeats(total_ids)
    if len(unique_ids) < len(total_ids):
        for current_id in unique_ids:
            if 1 < total_ids.count(current_id):
                violators.extend([_ for _ in components if id(_) == current_id])
    return violators, len(total_ids)


def check_empty_containers(argument) -> tuple[list, int]:
    r"""
    Checks empty containers.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> staff.append(abjad.Container())

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            {
            }
        }

        >>> violators, total = abjad.wf.check_empty_containers(staff)
        >>> violators
        [Container()]

    """
    violators, containers = [], set()
    for container in _iterate.components(argument, _score.Container):
        containers.add(container)
        if len(container) == 0:
            violators.append(container)
    return violators, len(containers)


def check_missing_parents(argument) -> tuple[list, int]:
    """
    Checks missing parents.
    """
    violators, total = [], set()
    components = _iterate.components(argument)
    for i, component in enumerate(components):
        total.add(component)
        if 0 < i:
            # BeforeGraceContainer._parent is always none;
            # so must use Parentage.parent,
            # which calls BeforeGraceContainer._get_parentage()
            if _parentage.Parentage(component).parent is None:
                violators.append(component)
    return violators, len(total)


def check_notes_on_wrong_clef(argument) -> tuple[list, int]:
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

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "alto"
                c'8
                d'8
                e'8
                f'8
            }

        >>> abjad.wf.check_notes_on_wrong_clef(staff)
        ([Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")], 4)

    ..  container:: example

        All instruments allow percussion clef:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> clef = abjad.Clef('percussion')
        >>> abjad.attach(clef, staff[0])
        >>> violin = abjad.Violin()
        >>> abjad.attach(violin, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "percussion"
                c'8
                d'8
                e'8
                f'8
            }

        >>> abjad.wf.check_notes_on_wrong_clef(staff)
        ([], 4)

    """
    violators, total = [], set()
    for leaf in _iterate.leaves(argument):
        total.add(leaf)
        instrument = _get.effective(leaf, _instruments.Instrument)
        if instrument is None:
            continue
        effective_clef = _get.effective(leaf, _indicators.Clef)
        if effective_clef is None:
            continue
        clefs = []
        for clef in instrument.clefs:
            if isinstance(clef, str):
                clef = _indicators.Clef(clef)
            assert isinstance(clef, _indicators.Clef), repr(clef)
            clefs.append(clef)
        clefs.append(_indicators.Clef("percussion"))
        if effective_clef not in clefs:
            violators.append(leaf)
    return violators, len(total)


def check_orphaned_dependent_wrappers(argument) -> tuple[list, int]:
    r"""
    Checks orphaned dependent wrappers.

    This should normally never happen because Abjad manages dependent wrappers
    behind the scenes.

    This check exists to make sure that any new code added to Abjad doesn't
    accidentally mangle dependent-wrapper handling.

    ..  container:: example

        >>> voice = abjad.Voice("c'8 [ d' e' f'")
        >>> assert len(voice._dependent_wrappers) == 1
        >>> wrapper = voice._dependent_wrappers[0]
        >>> wrapper
        Wrapper(annotation=None, context='Voice', deactivate=False, direction=None, indicator=StartBeam(), synthetic_offset=None, tag=Tag(string=''))

        >>> wrapper.component
        Note("c'8")

        >>> abjad.wf.check_orphaned_dependent_wrappers(voice)
        ([], 1)

        >>> voice[0:1] = [abjad.Note("cs'8")]
        >>> voice._dependent_wrappers
        []

        >>> abjad.wf.check_orphaned_dependent_wrappers(voice)
        ([], 0)

        >>> voice._dependent_wrappers.append(wrapper)
        >>> assert len(voice._dependent_wrappers) == 1
        >>> assert wrapper.component not in voice

        >>> abjad.wf.check_orphaned_dependent_wrappers(voice)
        ([Wrapper(annotation=None, context='Voice', deactivate=False, direction=None, indicator=StartBeam(), synthetic_offset=None, tag=Tag(string=''))], 1)

    """
    violators, total = [], 0
    for context in _iterate.components(argument, _score.Context):
        assert isinstance(context, _score.Context)
        for wrapper in context._dependent_wrappers:
            total += 1
            parentage = _get.parentage(wrapper.component)
            if context not in parentage:
                violators.append(wrapper)
    return violators, total


def check_out_of_range_pitches(
    argument, *, allow_indicators: typing.Sequence[str | enum.Enum] = ()
) -> tuple[list, int]:
    r"""
    Checks out-of-range notes.

    ..  container:: example

        Out of range:

        >>> staff = abjad.Staff("c'8 r8 <d fs>8 r8")
        >>> violin = abjad.Violin()
        >>> abjad.attach(violin, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                r8
                <d fs>8
                r8
            }

        >>> abjad.wf.check_out_of_range_pitches(staff)
        ([Chord('<d fs>8')], 2)

    ..  container:: example

        Using ``allow_indicators``:

        >>> staff = abjad.Staff("c'8 r8 <d fs>8 r8")
        >>> violin = abjad.Violin()
        >>> abjad.attach(violin, staff[0])
        >>> abjad.attach("ALLOW_OUT_OF_RANGE", staff[2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                r8
                <d fs>8
                r8
            }

        Does not check for indicator:

        >>> violators, total = abjad.wf.check_out_of_range_pitches(staff)
        >>> violators
        [Chord('<d fs>8')]

        Does check for indicator:

        >>> violators, total = abjad.wf.check_out_of_range_pitches(
        ...     staff, allow_indicators=["ALLOW_OUT_OF_RANGE"]
        ... )
        >>> violators
        []

    """
    violators, total = [], set()
    for leaf in _iterate.leaves(argument, pitched=True):
        total.add(leaf)
        ok = False
        for indicator in allow_indicators or ():
            if leaf._has_indicator(indicator):
                ok = True
        if ok is True:
            continue
        if "unpitched" in argument._get_indicators(str):
            continue
        instrument = _get.effective(leaf, _instruments.Instrument)
        if instrument is None:
            continue
        if not _iterpitches.sounding_pitches_are_in_range(leaf, instrument.pitch_range):
            violators.append(leaf)
    return violators, len(total)


def check_overlapping_beams(argument) -> tuple[list, int]:
    r"""
    Checks overlapping beams.

    ..  container:: example

        >>> voice = abjad.Voice("c'8 [ d' [ e' f' ]")
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \new Voice
        {
            c'8
            [
            d'8
            [
            e'8
            f'8
            ]
        }

        >>> abjad.wf.check_overlapping_beams(voice)
        ([Note("d'8")], 3)

        >>> voice = abjad.Voice("c'8 [ d' [ e' ] f' ]")
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \new Voice
        {
            c'8
            [
            d'8
            [
            e'8
            ]
            f'8
            ]
        }

        >>> abjad.wf.check_overlapping_beams(voice)
        ([Note("d'8")], 4)

        >>> voice = abjad.Voice("c'8 [ d' e' f' ]")
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            f'8
            ]
        }

        >>> abjad.wf.check_overlapping_beams(voice)
        ([], 2)

    """
    violators, total = [], 0
    context_name_to_wrappers = _aggregate_context_wrappers(argument)
    for _, wrappers in context_name_to_wrappers.items():
        wrappers.sort(key=lambda _: _get.timespan(_.component).start_offset)
        open_beam_count = 0
        for wrapper in wrappers:
            if _get.grace(wrapper.component) is True:
                continue
            total += 1
            if isinstance(wrapper.unbundle_indicator(), _indicators.StartBeam):
                open_beam_count += 1
            elif isinstance(wrapper.unbundle_indicator(), _indicators.StopBeam):
                open_beam_count -= 1
            if open_beam_count < 0 or 1 < open_beam_count:
                violators.append(wrapper.component)
    return violators, total


def check_overlapping_text_spanners(argument) -> tuple[list, int]:
    r"""
    Checks overlapping text spanners.

    Overlapping text spanners are not wellformed:

    ..  container:: example

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> abjad.text_spanner(voice)
        >>> abjad.text_spanner(voice[1:3])
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \new Voice
        {
            c'4
            \startTextSpan
            d'4
            \startTextSpan
            e'4
            \stopTextSpan
            f'4
            \stopTextSpan
        }

        >>> abjad.wf.check_overlapping_text_spanners(voice)
        ([Note("d'4")], 2)

    ..  container:: example

        Overlapping text spanners with different IDs are wellformed:

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> abjad.text_spanner(voice)
        >>> command = r'\startTextSpanOne'
        >>> start_text_span = abjad.StartTextSpan(command=command)
        >>> abjad.attach(start_text_span, voice[1])
        >>> command = r'\stopTextSpanOne'
        >>> stop_text_span = abjad.StopTextSpan(command=command)
        >>> abjad.attach(stop_text_span, voice[2])
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \new Voice
        {
            c'4
            \startTextSpan
            d'4
            \startTextSpanOne
            e'4
            \stopTextSpanOne
            f'4
            \stopTextSpan
        }

        >>> abjad.wf.check_overlapping_text_spanners(voice)
        ([], 2)

    ..  container:: example

        Enchained text spanners do not overlap (and are wellformed):

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> abjad.text_spanner(voice[:3])
        >>> abjad.text_spanner(voice[-2:])
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \new Voice
        {
            c'4
            \startTextSpan
            d'4
            e'4
            \stopTextSpan
            \startTextSpan
            f'4
            \stopTextSpan
        }

        >>> abjad.wf.check_overlapping_text_spanners(voice)
        ([], 2)

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

        >>> string = abjad.lilypond(voice)
        >>> print(string)
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

        >>> abjad.wf.check_overlapping_text_spanners(voice)
        ([], 2)

    """
    violators, total = [], 0

    def key(wrapper):
        if isinstance(wrapper.unbundle_indicator(), _indicators.StartTextSpan):
            priority = 1
        else:
            priority = 0
        return (wrapper.leaked_start_offset, priority)

    context_name_to_wrappers = _aggregate_context_wrappers(argument)
    for _, wrappers in context_name_to_wrappers.items():
        wrappers.sort(key=key)
        open_spanners: dict = {}
        for wrapper in wrappers:
            if wrapper.deactivate is True:
                continue
            if isinstance(wrapper.unbundle_indicator(), _indicators.StartTextSpan):
                total += 1
                command = wrapper.unbundle_indicator().command
                command = command.replace("start", "")
                command = command.replace("Start", "")
                if command not in open_spanners:
                    open_spanners[command] = []
                if open_spanners[command]:
                    violators.append(wrapper.component)
                open_spanners[command].append(wrapper.component)
            elif isinstance(wrapper.unbundle_indicator(), _indicators.StopTextSpan):
                command = wrapper.unbundle_indicator().command
                command = command.replace("stop", "")
                command = command.replace("Stop", "")
                if command in open_spanners and open_spanners[command]:
                    open_spanners[command].pop()
    return violators, total


def check_unmatched_stop_text_spans(argument) -> tuple[list, int]:
    r"""
    Checks unmatched stop text spans.

    ..  container:: example

        Unmatched stop text span is not wellformed:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, voice[-1])
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \new Voice
        {
            c'4
            c'4
            c'4
            c'4
            \stopTextSpan
        }

        >>> abjad.wf.check_unmatched_stop_text_spans(voice)
        ([Note("c'4")], 0)

        Matched stop text span is wellformed:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> start_text_span = abjad.StartTextSpan()
        >>> abjad.attach(start_text_span, voice[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, voice[-1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \startTextSpan
                c'4
                c'4
                c'4
                \stopTextSpan
            }

        >>> abjad.wf.wellformed(voice)
        True

    """
    violators, total = [], 0
    context_name_to_wrappers = _aggregate_context_wrappers(argument)
    for _, wrappers in context_name_to_wrappers.items():
        wrappers.sort(key=lambda _: _.leaked_start_offset)
        open_spanners: dict = {}
        for wrapper in wrappers:
            if isinstance(wrapper.unbundle_indicator(), _indicators.StartTextSpan):
                total += 1
                command = wrapper.unbundle_indicator().command
                command = command.replace("start", "")
                command = command.replace("Start", "")
                if command not in open_spanners:
                    open_spanners[command] = []
                open_spanners[command].append(wrapper.component)
            elif isinstance(wrapper.unbundle_indicator(), _indicators.StopTextSpan):
                command = wrapper.unbundle_indicator().command
                command = command.replace("stop", "")
                command = command.replace("Stop", "")
                if command not in open_spanners or not open_spanners[command]:
                    violators.append(wrapper.component)
                else:
                    open_spanners[command].pop()
    return violators, total


def check_unterminated_hairpins(argument) -> tuple[list, int]:
    r"""
    Checks unterminated hairpins.

    ..  container:: example

        Unterminated crescendo is not wellformed:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> start_hairpin = abjad.StartHairpin('<')
        >>> abjad.attach(start_hairpin, voice[0])
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \new Voice
        {
            c'4
            \<
            c'4
            c'4
            c'4
        }

        >>> abjad.wf.check_unterminated_hairpins(voice)
        ([Note("c'4")], 1)

        Even with start dynamic:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> dynamic = abjad.Dynamic('f')
        >>> abjad.attach(dynamic, voice[0])
        >>> start_hairpin = abjad.StartHairpin('<')
        >>> abjad.attach(start_hairpin, voice[0])
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \new Voice
        {
            c'4
            \f
            \<
            c'4
            c'4
            c'4
        }

        >>> abjad.wf.check_unterminated_hairpins(voice)
        ([Note("c'4")], 1)

        Terminated crescendo is wellformed:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> start_hairpin = abjad.StartHairpin('<')
        >>> abjad.attach(start_hairpin, voice[0])
        >>> dynamic = abjad.Dynamic('f')
        >>> abjad.attach(dynamic, voice[-1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \<
                c'4
                c'4
                c'4
                \f
            }

        >>> abjad.wf.wellformed(voice)
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

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \<
                c'4
                c'4
                c'4
                \!
            }

        >>> abjad.wf.wellformed(voice)
        True

    """
    violators, total = [], 0
    context_name_to_wrappers = _aggregate_context_wrappers(argument)
    for _, wrappers in context_name_to_wrappers.items():
        last_dynamic = None
        last_tag = _tag.Tag()
        wrappers.sort(key=lambda _: _.leaked_start_offset)
        for wrapper in wrappers:
            parameter = getattr(wrapper.unbundle_indicator(), "parameter", None)
            if parameter == "DYNAMIC" or isinstance(
                wrapper.unbundle_indicator(), _indicators.StopHairpin
            ):
                last_dynamic = wrapper.unbundle_indicator()
                last_tag = wrapper.tag
                if isinstance(wrapper.unbundle_indicator(), _indicators.StartHairpin):
                    total += 1
        if (
            isinstance(last_dynamic, _indicators.StartHairpin)
            and _tag.Tag("RIGHT_BROKEN").string not in last_tag.string
        ):
            violators.append(wrapper.component)
    return violators, total


def check_unterminated_text_spanners(argument) -> tuple[list, int]:
    r"""
    Checks unterminated text spanners.

    ..  container:: example

        Unterminated text spanner is not wellformed:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> start_text_span = abjad.StartTextSpan()
        >>> abjad.attach(start_text_span, voice[0])
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \new Voice
        {
            c'4
            \startTextSpan
            c'4
            c'4
            c'4
        }

        >>> abjad.wf.check_unterminated_text_spanners(voice)
        ([Note("c'4")], 1)

        Terminated text span is wellformed:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> start_text_span = abjad.StartTextSpan()
        >>> abjad.attach(start_text_span, voice[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, voice[-1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \startTextSpan
                c'4
                c'4
                c'4
                \stopTextSpan
            }

        >>> abjad.wf.wellformed(voice)
        True

    """
    violators, total = [], 0
    context_name_to_wrappers = _aggregate_context_wrappers(argument)
    for _, wrappers in context_name_to_wrappers.items():
        wrappers.sort(key=lambda _: _.leaked_start_offset)
        open_spanners: dict = {}
        for wrapper in wrappers:
            if wrapper.deactivate is True:
                continue
            if isinstance(wrapper.unbundle_indicator(), _indicators.StartTextSpan):
                total += 1
                command = wrapper.unbundle_indicator().command
                command = command.replace("start", "")
                command = command.replace("Start", "")
                if command not in open_spanners:
                    open_spanners[command] = []
                open_spanners[command].append(wrapper.component)
            elif isinstance(wrapper.unbundle_indicator(), _indicators.StopTextSpan):
                command = wrapper.unbundle_indicator().command
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


_globals = globals()


def _call_functions(
    component,
    check_beamed_lone_notes: bool = True,
    check_beamed_long_notes: bool = True,
    check_duplicate_ids: bool = True,
    check_empty_containers: bool = True,
    check_missing_parents: bool = True,
    check_notes_on_wrong_clef: bool = True,
    check_orphaned_dependent_wrappers: bool = True,
    check_out_of_range_pitches: bool = True,
    check_overlapping_beams: bool = True,
    check_overlapping_text_spanners: bool = True,
    check_unmatched_stop_text_spans: bool = True,
    check_unterminated_hairpins: bool = True,
    check_unterminated_text_spanners: bool = True,
):
    triples = []
    if check_beamed_lone_notes:
        name = "check_beamed_lone_notes"
        violators, count = _globals[name](component)
        triples.append((violators, count, name))
    if check_beamed_long_notes:
        name = "check_beamed_long_notes"
        violators, count = _globals[name](component)
        triples.append((violators, count, name))
    if check_duplicate_ids:
        name = "check_duplicate_ids"
        violators, count = _globals[name](component)
        triples.append((violators, count, name))
    if check_empty_containers:
        name = "check_empty_containers"
        violators, count = _globals[name](component)
        triples.append((violators, count, name))
    if check_missing_parents:
        name = "check_missing_parents"
        violators, count = _globals[name](component)
        triples.append((violators, count, name))
    if check_notes_on_wrong_clef:
        name = "check_notes_on_wrong_clef"
        violators, count = _globals[name](component)
        triples.append((violators, count, name))
    if check_orphaned_dependent_wrappers:
        name = "check_orphaned_dependent_wrappers"
        violators, count = _globals[name](component)
        triples.append((violators, count, name))
    if check_out_of_range_pitches:
        name = "check_out_of_range_pitches"
        violators, count = _globals[name](component)
        triples.append((violators, count, name))
    if check_overlapping_beams:
        name = "check_overlapping_beams"
        violators, count = _globals[name](component)
        triples.append((violators, count, name))
    if check_overlapping_text_spanners:
        name = "check_overlapping_text_spanners"
        violators, count = _globals[name](component)
        triples.append((violators, count, name))
    if check_unmatched_stop_text_spans:
        name = "check_unmatched_stop_text_spans"
        violators, count = _globals[name](component)
        triples.append((violators, count, name))
    if check_unterminated_hairpins:
        name = "check_unterminated_hairpins"
        violators, count = _globals[name](component)
        triples.append((violators, count, name))
    if check_unterminated_text_spanners:
        name = "check_unterminated_text_spanners"
        violators, count = _globals[name](component)
        triples.append((violators, count, name))
    return triples


def tabulate_wellformedness(
    component,
    check_beamed_lone_notes: bool = True,
    check_beamed_long_notes: bool = True,
    check_duplicate_ids: bool = True,
    check_empty_containers: bool = True,
    check_missing_parents: bool = True,
    check_notes_on_wrong_clef: bool = True,
    check_orphaned_dependent_wrappers: bool = True,
    check_out_of_range_pitches: bool = True,
    check_overlapping_beams: bool = True,
    check_overlapping_text_spanners: bool = True,
    check_unmatched_stop_text_spans: bool = True,
    check_unterminated_hairpins: bool = True,
    check_unterminated_text_spanners: bool = True,
) -> tuple[int, str]:
    """
    Tabulates wellformedness.
    """
    triples = _call_functions(
        component,
        check_beamed_lone_notes=check_beamed_lone_notes,
        check_beamed_long_notes=check_beamed_long_notes,
        check_duplicate_ids=check_duplicate_ids,
        check_empty_containers=check_empty_containers,
        check_missing_parents=check_missing_parents,
        check_notes_on_wrong_clef=check_notes_on_wrong_clef,
        check_orphaned_dependent_wrappers=check_orphaned_dependent_wrappers,
        check_out_of_range_pitches=check_out_of_range_pitches,
        check_overlapping_beams=check_overlapping_beams,
        check_overlapping_text_spanners=check_overlapping_text_spanners,
        check_unmatched_stop_text_spans=check_unmatched_stop_text_spans,
        check_unterminated_hairpins=check_unterminated_hairpins,
        check_unterminated_text_spanners=check_unterminated_text_spanners,
    )
    strings = []
    total_violators = 0
    for violators, total, name in triples:
        violator_count = len(violators)
        name = name.replace("check_", "")
        name = name.replace("_", " ")
        string = f"{violator_count} /    {total} {name}"
        strings.append(string)
        total_violators += violator_count
    return total_violators, "\n".join(strings)


def wellformed(
    component,
    check_beamed_lone_notes: bool = True,
    check_beamed_long_notes: bool = True,
    check_duplicate_ids: bool = True,
    check_empty_containers: bool = True,
    check_missing_parents: bool = True,
    check_notes_on_wrong_clef: bool = True,
    check_orphaned_dependent_wrappers: bool = True,
    check_out_of_range_pitches: bool = True,
    check_overlapping_beams: bool = True,
    check_overlapping_text_spanners: bool = True,
    check_unmatched_stop_text_spans: bool = True,
    check_unterminated_hairpins: bool = True,
    check_unterminated_text_spanners: bool = True,
) -> bool:
    """
    Is true when ``component`` is wellformed.
    """
    triples = _call_functions(
        component,
        check_beamed_lone_notes=check_beamed_lone_notes,
        check_beamed_long_notes=check_beamed_long_notes,
        check_duplicate_ids=check_duplicate_ids,
        check_empty_containers=check_empty_containers,
        check_missing_parents=check_missing_parents,
        check_notes_on_wrong_clef=check_notes_on_wrong_clef,
        check_orphaned_dependent_wrappers=check_orphaned_dependent_wrappers,
        check_out_of_range_pitches=check_out_of_range_pitches,
        check_overlapping_beams=check_overlapping_beams,
        check_overlapping_text_spanners=check_overlapping_text_spanners,
        check_unmatched_stop_text_spans=check_unmatched_stop_text_spans,
        check_unterminated_hairpins=check_unterminated_hairpins,
        check_unterminated_text_spanners=check_unterminated_text_spanners,
    )
    for violators, total, name in triples:
        if violators:
            return False
    return True
