import typing

from . import _inspect
from .duration import Duration
from .indicators.Clef import Clef
from .indicators.StartBeam import StartBeam
from .indicators.StartHairpin import StartHairpin
from .indicators.StartTextSpan import StartTextSpan
from .indicators.StopBeam import StopBeam
from .indicators.StopHairpin import StopHairpin
from .indicators.StopTextSpan import StopTextSpan
from .instruments import Instrument
from .iterate import Iteration
from .iterpitches import sounding_pitches_are_in_range
from .parentage import Parentage
from .score import Container, Context
from .sequence import Sequence
from .tag import Tag

### PRIVATE FUNCTIONS ###


def _aggregate_context_wrappers(argument):
    """
    Special_Voice may contain other instances of Special_Voice.
    This currently happens with OnBeatGraceContainer.
    This method aggregates all Special_Voice wrappers for checks.
    """
    name_to_wrappers: typing.Dict = {}
    for context in Iteration(argument).components(Context):
        if context.name not in name_to_wrappers:
            name_to_wrappers[context.name] = []
        wrappers = context._dependent_wrappers[:]
        name_to_wrappers[context.name].extend(wrappers)
    return name_to_wrappers


### PUBLIC FUNCTIONS ###


def check_beamed_long_notes(argument) -> typing.Tuple[typing.List, int]:
    r"""
    Checks beamed long notes.

    ..  container:: example

        Beamed quarter notes are not wellformed:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> abjad.attach(abjad.StartBeam(), voice[0])
        >>> abjad.attach(abjad.StopBeam(), voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> print(abjad.lilypond(voice))
            \new Voice
            {
                c'4
                [
                d'4
                ]
                e'4
                f'4
            }

        >>> print(abjad.wf.tabulate_wellformedness(voice))
        2 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        0 /     4 notes on wrong clef
        0 /     4 out of range pitches
        0 /     0 overlapping text spanners
        0 /     0 unmatched stop text spans
        0 /     0 unterminated hairpins
        0 /     0 unterminated text spanners

        Beamed eighth notes are wellformed:

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8")
        >>> abjad.attach(abjad.StartBeam(), voice[0])
        >>> abjad.attach(abjad.StopBeam(), voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> print(abjad.lilypond(voice))
            \new Voice
            {
                c'8
                [
                d'8
                ]
                e'8
                f'8
            }

        >>> print(abjad.wf.tabulate_wellformedness(voice))
        0 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        0 /     4 notes on wrong clef
        0 /     4 out of range pitches
        0 /     0 overlapping text spanners
        0 /     0 unmatched stop text spans
        0 /     0 unterminated hairpins
        0 /     0 unterminated text spanners

    ..  container:: example

        REGRESSION. Matching start- and stop-beam indicators work
        correctly:

        >>> voice = abjad.Voice("c'8 d'8 e'4 f'2")
        >>> abjad.attach(abjad.StartBeam(), voice[0])
        >>> abjad.attach(abjad.StopBeam(), voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> print(abjad.lilypond(voice))
            \new Voice
            {
                c'8
                [
                d'8
                ]
                e'4
                f'2
            }

        >>> print(abjad.wf.tabulate_wellformedness(voice))
        0 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        0 /     4 notes on wrong clef
        0 /     4 out of range pitches
        0 /     0 overlapping text spanners
        0 /     0 unmatched stop text spans
        0 /     0 unterminated hairpins
        0 /     0 unterminated text spanners

    The examples above feature Abjad voice containers because beams are
    voice-persistent.
    """
    violators, total = [], 0
    for leaf in Iteration(argument).leaves():
        total += 1
        if leaf.written_duration < Duration((1, 4)):
            continue
        start_wrapper = _inspect._get_effective(leaf, StartBeam, unwrap=False)
        if start_wrapper is None:
            continue
        stop_wrapper = _inspect._get_effective(leaf, StopBeam, unwrap=False)
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


def check_duplicate_ids(argument) -> typing.Tuple[typing.List, int]:
    """
    Checks duplicate IDs.
    """
    violators = []
    components = Iteration(argument).components()
    total_ids = [id(_) for _ in components]
    unique_ids = Sequence(total_ids).remove_repeats()
    if len(unique_ids) < len(total_ids):
        for current_id in unique_ids:
            if 1 < total_ids.count(current_id):
                violators.extend([_ for _ in components if id(_) == current_id])
    return violators, len(total_ids)


def check_empty_containers(argument) -> typing.Tuple[typing.List, int]:
    r"""
    Checks empty containers.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> staff.append(abjad.Container())

        >>> print(abjad.lilypond(staff))
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
    for container in Iteration(argument).components(Container):
        containers.add(container)
        if len(container) == 0:
            violators.append(container)
    return violators, len(containers)


def check_missing_parents(argument) -> typing.Tuple[typing.List, int]:
    """
    Checks missing parents.
    """
    violators, total = [], set()
    components = Iteration(argument).components()
    for i, component in enumerate(components):
        total.add(component)
        if 0 < i:
            # TODO: figure out why "if component._parent is None" doesn't work
            if Parentage(component).parent is None:
                violators.append(component)
    return violators, len(total)


def check_notes_on_wrong_clef(argument) -> typing.Tuple[typing.List, int]:
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

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                \clef "alto"
                c'8
                d'8
                e'8
                f'8
            }

        >>> print(abjad.wf.tabulate_wellformedness(staff))
        0 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        4 /     4 notes on wrong clef
        0 /     4 out of range pitches
        0 /     0 overlapping text spanners
        0 /     0 unmatched stop text spans
        0 /     0 unterminated hairpins
        0 /     0 unterminated text spanners

    ..  container:: example

        Always allows percussion clef:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> clef = abjad.Clef('percussion')
        >>> abjad.attach(clef, staff[0])
        >>> violin = abjad.Violin()
        >>> abjad.attach(violin, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                \clef "percussion"
                c'8
                d'8
                e'8
                f'8
            }

        >>> print(abjad.wf.tabulate_wellformedness(staff))
        0 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        0 /     4 notes on wrong clef
        0 /     4 out of range pitches
        0 /     0 overlapping text spanners
        0 /     0 unmatched stop text spans
        0 /     0 unterminated hairpins
        0 /     0 unterminated text spanners

    """
    violators, total = [], set()
    for leaf in Iteration(argument).leaves():
        total.add(leaf)
        instrument = _inspect._get_effective(leaf, Instrument)
        if instrument is None:
            continue
        clef = _inspect._get_effective(leaf, Clef)
        if clef is None:
            continue
        allowable_clefs = [Clef(_) for _ in instrument.allowable_clefs]
        allowable_clefs.append(Clef("percussion"))
        if clef not in allowable_clefs:
            violators.append(leaf)
    return violators, len(total)


def check_out_of_range_pitches(argument) -> typing.Tuple[typing.List, int]:
    r"""
    Checks out-of-range notes.

    ..  container:: example

        Out of range:

        >>> staff = abjad.Staff("c'8 r8 <d fs>8 r8")
        >>> violin = abjad.Violin()
        >>> abjad.attach(violin, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'8
                r8
                <d fs>8
                r8
            }

        >>> print(abjad.wf.tabulate_wellformedness(staff))
        0 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        0 /     4 notes on wrong clef
        1 /     2 out of range pitches
        0 /     0 overlapping text spanners
        0 /     0 unmatched stop text spans
        0 /     0 unterminated hairpins
        0 /     0 unterminated text spanners

    ..  container:: example

        Allows out-of-range pitches:

        >>> staff = abjad.Staff("c'8 r8 <d fs>8 r8")
        >>> violin = abjad.Violin()
        >>> abjad.attach(violin, staff[0])
        >>> abjad.attach("ALLOW_OUT_OF_RANGE", staff[2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'8
                r8
                <d fs>8
                r8
            }

        >>> print(abjad.wf.tabulate_wellformedness(staff))
        0 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        0 /     4 notes on wrong clef
        0 /     2 out of range pitches
        0 /     0 overlapping text spanners
        0 /     0 unmatched stop text spans
        0 /     0 unterminated hairpins
        0 /     0 unterminated text spanners

    """
    violators, total = [], set()
    for leaf in Iteration(argument).leaves(pitched=True):
        total.add(leaf)
        if leaf._has_indicator("ALLOW_OUT_OF_RANGE"):
            continue
        if leaf._has_indicator("HIDDEN"):
            continue
        if "unpitched" in argument._get_indicators(str):
            continue
        instrument = _inspect._get_effective(leaf, Instrument)
        if instrument is None:
            continue
        # if leaf not in instrument.pitch_range:
        if not sounding_pitches_are_in_range(leaf, instrument.pitch_range):
            violators.append(leaf)
    return violators, len(total)


def check_overlapping_text_spanners(argument) -> typing.Tuple[typing.List, int]:
    r"""
    Checks overlapping text spanners.

    ..  container:: example

        Overlapping text spanners are not wellformed:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> abjad.text_spanner(voice)
        >>> abjad.text_spanner(voice[1:3])
        >>> print(abjad.lilypond(voice))
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

        >>> print(abjad.wf.tabulate_wellformedness(voice))
        0 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        0 /     4 notes on wrong clef
        0 /     4 out of range pitches
        1 /     2 overlapping text spanners
        0 /     2 unmatched stop text spans
        0 /     0 unterminated hairpins
        0 /     2 unterminated text spanners

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
        >>> print(abjad.lilypond(voice))
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

        >>> print(abjad.wf.tabulate_wellformedness(voice))
        0 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        0 /     4 notes on wrong clef
        0 /     4 out of range pitches
        0 /     2 overlapping text spanners
        0 /     2 unmatched stop text spans
        0 /     0 unterminated hairpins
        0 /     2 unterminated text spanners

    ..  container:: example

        Enchained text spanners do not overlap (and are wellformed):

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> abjad.text_spanner(voice[:3])
        >>> abjad.text_spanner(voice[-2:])
        >>> print(abjad.lilypond(voice))
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

        >>> print(abjad.wf.tabulate_wellformedness(voice))
        0 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        0 /     4 notes on wrong clef
        0 /     4 out of range pitches
        0 /     2 overlapping text spanners
        0 /     2 unmatched stop text spans
        0 /     0 unterminated hairpins
        0 /     2 unterminated text spanners

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

        >>> print(abjad.lilypond(voice))
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

        >>> print(abjad.wf.tabulate_wellformedness(voice))
        0 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        0 /     4 notes on wrong clef
        0 /     4 out of range pitches
        0 /     2 overlapping text spanners
        0 /     2 unmatched stop text spans
        0 /     0 unterminated hairpins
        0 /     2 unterminated text spanners

    """
    violators, total = [], 0

    def key(wrapper):
        if isinstance(wrapper.indicator, StartTextSpan):
            priority = 1
        else:
            priority = 0
        return (wrapper.leaked_start_offset, priority)

    name_to_wrappers = _aggregate_context_wrappers(argument)
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


def check_unmatched_stop_text_spans(argument) -> typing.Tuple[typing.List, int]:
    r"""
    Checks unmatched stop text spans.

    ..  container:: example

        Unmatched stop text span is not wellformed:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, voice[-1])
        >>> print(abjad.lilypond(voice))
        \new Voice
        {
            c'4
            c'4
            c'4
            c'4
            \stopTextSpan
        }

        >>> print(abjad.wf.tabulate_wellformedness(voice))
        0 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        0 /     4 notes on wrong clef
        0 /     4 out of range pitches
        0 /     0 overlapping text spanners
        1 /     0 unmatched stop text spans
        0 /     0 unterminated hairpins
        0 /     0 unterminated text spanners

        Matched stop text span is wellformed:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> start_text_span = abjad.StartTextSpan()
        >>> abjad.attach(start_text_span, voice[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, voice[-1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> print(abjad.lilypond(voice))
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
    name_to_wrappers = _aggregate_context_wrappers(argument)
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


def check_unterminated_hairpins(argument) -> typing.Tuple[typing.List, int]:
    r"""
    Checks unterminated hairpins.

    ..  container:: example

        Unterminated crescendo is not wellformed:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> start_hairpin = abjad.StartHairpin('<')
        >>> abjad.attach(start_hairpin, voice[0])
        >>> print(abjad.lilypond(voice))
        \new Voice
        {
            c'4
            \<
            c'4
            c'4
            c'4
        }

        >>> print(abjad.wf.tabulate_wellformedness(voice))
        0 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        0 /     4 notes on wrong clef
        0 /     4 out of range pitches
        0 /     0 overlapping text spanners
        0 /     0 unmatched stop text spans
        1 /     1 unterminated hairpins
        0 /     0 unterminated text spanners

        Even with start dynamic:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> dynamic = abjad.Dynamic('f')
        >>> abjad.attach(dynamic, voice[0])
        >>> start_hairpin = abjad.StartHairpin('<')
        >>> abjad.attach(start_hairpin, voice[0])
        >>> print(abjad.lilypond(voice))
        \new Voice
        {
            c'4
            \f
            \<
            c'4
            c'4
            c'4
        }

        >>> print(abjad.wf.tabulate_wellformedness(voice))
        0 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        0 /     4 notes on wrong clef
        0 /     4 out of range pitches
        0 /     0 overlapping text spanners
        0 /     0 unmatched stop text spans
        1 /     1 unterminated hairpins
        0 /     0 unterminated text spanners

        Terminated crescendo is wellformed:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> start_hairpin = abjad.StartHairpin('<')
        >>> abjad.attach(start_hairpin, voice[0])
        >>> dynamic = abjad.Dynamic('f')
        >>> abjad.attach(dynamic, voice[-1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> print(abjad.lilypond(voice))
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

            >>> print(abjad.lilypond(voice))
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
    name_to_wrappers = _aggregate_context_wrappers(argument)
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
            Tag("RIGHT_BROKEN")
        ) not in str(last_tag):
            violators.append(wrapper.component)
    return violators, total


def check_unterminated_text_spanners(argument) -> typing.Tuple[typing.List, int]:
    r"""
    Checks unterminated text spanners.

    ..  container:: example

        Unterminated text spanner is not wellformed:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> start_text_span = abjad.StartTextSpan()
        >>> abjad.attach(start_text_span, voice[0])
        >>> print(abjad.lilypond(voice))
        \new Voice
        {
            c'4
            \startTextSpan
            c'4
            c'4
            c'4
        }

        >>> print(abjad.wf.tabulate_wellformedness(voice))
        0 /     4 beamed long notes
        0 /     5 duplicate ids
        0 /     1 empty containers
        0 /     5 missing parents
        0 /     4 notes on wrong clef
        0 /     4 out of range pitches
        0 /     1 overlapping text spanners
        0 /     1 unmatched stop text spans
        0 /     0 unterminated hairpins
        1 /     1 unterminated text spanners

        Terminated text span is wellformed:

        >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
        >>> start_text_span = abjad.StartTextSpan()
        >>> abjad.attach(start_text_span, voice[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, voice[-1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> print(abjad.lilypond(voice))
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
    name_to_wrappers = _aggregate_context_wrappers(argument)
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


_globals = globals()


def _call_functions(
    component,
    check_beamed_long_notes: bool = True,
    check_duplicate_ids: bool = True,
    check_empty_containers: bool = True,
    check_missing_parents: bool = True,
    check_notes_on_wrong_clef: bool = True,
    check_out_of_range_pitches: bool = True,
    check_overlapping_text_spanners: bool = True,
    check_unmatched_stop_text_spans: bool = True,
    check_unterminated_hairpins: bool = True,
    check_unterminated_text_spanners: bool = True,
):
    triples = []
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
    if check_out_of_range_pitches:
        name = "check_out_of_range_pitches"
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
    check_beamed_long_notes: bool = True,
    check_duplicate_ids: bool = True,
    check_empty_containers: bool = True,
    check_missing_parents: bool = True,
    check_notes_on_wrong_clef: bool = True,
    check_out_of_range_pitches: bool = True,
    check_overlapping_text_spanners: bool = True,
    check_unmatched_stop_text_spans: bool = True,
    check_unterminated_hairpins: bool = True,
    check_unterminated_text_spanners: bool = True,
) -> str:
    """
    Tabulates wellformedness.
    """
    triples = _call_functions(
        component,
        check_beamed_long_notes=check_beamed_long_notes,
        check_duplicate_ids=check_duplicate_ids,
        check_empty_containers=check_empty_containers,
        check_missing_parents=check_missing_parents,
        check_notes_on_wrong_clef=check_notes_on_wrong_clef,
        check_out_of_range_pitches=check_out_of_range_pitches,
        check_overlapping_text_spanners=check_overlapping_text_spanners,
        check_unmatched_stop_text_spans=check_unmatched_stop_text_spans,
        check_unterminated_hairpins=check_unterminated_hairpins,
        check_unterminated_text_spanners=check_unterminated_text_spanners,
    )
    strings = []
    for violators, total, name in triples:
        violator_count = len(violators)
        name = name.replace("check_", "")
        name = name.replace("_", " ")
        string = f"{violator_count} /    {total} {name}"
        strings.append(string)
    return "\n".join(strings)


def wellformed(
    component,
    check_beamed_long_notes: bool = True,
    check_duplicate_ids: bool = True,
    check_empty_containers: bool = True,
    check_missing_parents: bool = True,
    check_notes_on_wrong_clef: bool = True,
    check_out_of_range_pitches: bool = True,
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
        check_beamed_long_notes=check_beamed_long_notes,
        check_duplicate_ids=check_duplicate_ids,
        check_empty_containers=check_empty_containers,
        check_missing_parents=check_missing_parents,
        check_notes_on_wrong_clef=check_notes_on_wrong_clef,
        check_out_of_range_pitches=check_out_of_range_pitches,
        check_overlapping_text_spanners=check_overlapping_text_spanners,
        check_unmatched_stop_text_spans=check_unmatched_stop_text_spans,
        check_unterminated_hairpins=check_unterminated_hairpins,
        check_unterminated_text_spanners=check_unterminated_text_spanners,
    )
    for violators, total, name in triples:
        if violators:
            return False
    return True
