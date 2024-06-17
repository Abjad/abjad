import copy
import dataclasses
import typing

from . import bind as _bind
from . import duration as _duration
from . import enums as _enums
from . import format as _format
from . import get as _get
from . import indicators as _indicators
from . import iterate as _iterate
from . import lilypondfile as _lilypondfile
from . import makers as _makers
from . import metricmodulation as _metricmodulation
from . import overrides as _overrides
from . import pcollections as _pcollections
from . import pitch as _pitch
from . import score as _score
from . import select as _select
from . import spanners as _spanners
from . import tag as _tag
from . import timespan as _timespan


def _illustrate_component(component):
    block = _lilypondfile.Block(name="score")
    block.items.append(component)
    lilypond_file = _lilypondfile.LilyPondFile([block])
    return lilypond_file


def _illustrate_markup(markup):
    lilypond_file = _lilypondfile.LilyPondFile()
    markup = dataclasses.replace(markup)
    lilypond_file.items.append(markup)
    return lilypond_file


def _illustrate_markup_maker(argument, **keywords):
    markup = argument._make_markup(**keywords)
    return _illustrate_markup(markup)


def _illustrate_metric_modulation(metric_modulation):
    lilypond_file = _lilypondfile.LilyPondFile()
    markup = metric_modulation._get_markup()
    lilypond_file.items.append(markup)
    return lilypond_file


def _illustrate_pitch_class_set(set_):
    chord = _score.Chord(set_, _duration.Duration(1))
    voice = _score.Voice([chord], name="Voice")
    staff = _score.Staff([voice], name="Staff")
    score = _score.Score([staff], name="Score")
    lilypond_file = _lilypondfile.LilyPondFile([score])
    return lilypond_file


def _illustrate_pitch_range(range_):
    start_pitch = _pitch.NamedPitch(range_.start_pitch)
    stop_pitch = _pitch.NamedPitch(range_.stop_pitch)
    start_pitch_clef = _indicators.Clef.from_pitches([start_pitch])
    stop_pitch_clef = _indicators.Clef.from_pitches([stop_pitch])
    start_note = _score.Note(range_.start_pitch, 1)
    stop_note = _score.Note(range_.stop_pitch, 1)
    if start_pitch_clef == stop_pitch_clef:
        if start_pitch_clef == _indicators.Clef("bass"):
            bass_voice = _score.Voice(name="Bass_Voice")
            bass_staff = _score.Staff([bass_voice], name="Bass_Staff")
            bass_voice.extend([start_note, stop_note])
            _bind.attach(_indicators.Clef("bass"), start_note)
            bass_leaves = _select.leaves(bass_voice)
            _spanners.glissando(bass_leaves)
            score = _score.Score([bass_staff], name="Score")
        else:
            treble_voice = _score.Voice(name="Treble_Voice")
            treble_staff = _score.Staff([treble_voice], name="Treble_Staff")
            treble_voice.extend([start_note, stop_note])
            _bind.attach(_indicators.Clef("treble"), start_note)
            treble_leaves = _select.leaves(treble_voice)
            _spanners.glissando(treble_leaves)
            score = _score.Score([treble_staff], name="Score")
    else:
        score = make_piano_score()
        treble_voice, bass_voice = score["Treble_Voice"], score["Bass_Voice"]
        bass_voice.extend([start_note, stop_note])
        treble_voice.extend("s1 s1")
        bass_leaves = _select.leaves(bass_voice)
        _spanners.glissando(bass_leaves)
        _bind.attach(_indicators.StaffChange("Treble_Staff"), bass_voice[1])
        _bind.attach(_indicators.Clef("treble"), treble_voice[0])
        _bind.attach(_indicators.Clef("bass"), bass_voice[0])
    for leaf in _iterate.leaves(score):
        leaf.multiplier = (1, 4)
    _overrides.override(score).BarLine.stencil = False
    _overrides.override(score).SpanBar.stencil = False
    _overrides.override(score).Glissando.thickness = 2
    _overrides.override(score).TimeSignature.stencil = False
    lilypond_file = _lilypondfile.LilyPondFile([score])
    return lilypond_file


def _illustrate_pitch_segment(segment):
    named_pitches = [_pitch.NamedPitch(x) for x in segment]
    notes = _makers.make_notes(named_pitches, [1])
    score = make_piano_score(leaves=notes)
    _overrides.override(score).TimeSignature.stencil = False
    _overrides.override(score).BarLine.stencil = False
    _overrides.override(score).SpanBar.stencil = False
    for leaf in _iterate.leaves(score):
        leaf.multiplier = (1, 8)
    _overrides.override(score).Rest.transparent = True
    lilypond_file = _lilypondfile.LilyPondFile([score])
    return lilypond_file


def _illustrate_pitch_set(set_):
    upper, lower = [], []
    for pitch in set_:
        if pitch < 0:
            lower.append(pitch)
        else:
            upper.append(pitch)
    if upper:
        upper = _score.Chord(upper, _duration.Duration(1))
    else:
        upper = _score.Skip((1, 1))
    if lower:
        lower = _score.Chord(lower, _duration.Duration(1))
    else:
        lower = _score.Skip((1, 1))
    upper_voice = _score.Voice([upper], name="Treble_Voice")
    upper_staff = _score.Staff([upper_voice], name="Treble_Staff")
    lower_voice = _score.Voice([lower], name="Bass_Voice")
    lower_staff = _score.Staff([lower_voice], name="Bass_Staff")
    staff_group = _score.StaffGroup(
        [upper_staff, lower_staff],
        lilypond_type="PianoStaff",
        name="Piano_Staff",
    )
    score = _score.Score([staff_group], name="Score")
    lilypond_file = _lilypondfile.LilyPondFile([score])
    return lilypond_file


def _illustrate_pitch_class_segment(
    segment, markup_direction=_enums.UP, figure_name=None
):
    notes = []
    for item in segment:
        note = _score.Note(item, _duration.Duration(1, 8))
        notes.append(note)
    markup = None
    if isinstance(figure_name, str):
        figure_name = _indicators.Markup(rf"\markup {figure_name}")
    if figure_name is not None:
        markup = figure_name
    if markup is not None:
        direction = markup_direction
        markup = dataclasses.replace(markup, direction=direction)
        _bind.attach(markup, notes[0])
    voice = _score.Voice(notes, name="Voice")
    staff = _score.Staff([voice], name="Staff")
    score = _score.Score([staff], name="Score")
    preamble = r"""\layout {
    \accidentalStyle forget
    indent = 0
    \context {
        \Score
        \override BarLine.transparent = ##t
        \override BarNumber.stencil = ##f
        \override Beam.stencil = ##f
        \override Flag.stencil = ##f
        \override Stem.stencil = ##f
        \override TimeSignature.stencil = ##f
        proportionalNotationDuration = \musicLength 1*1/12
    }
}

\paper {
    markup-system-spacing.padding = 8
    system-system-spacing.padding = 10
    top-markup-spacing.padding = 4
}"""
    leaf = _select.leaf(score, -1)
    bar_line = _indicators.BarLine("|.")
    _bind.attach(bar_line, leaf)
    string = r"\override Score.BarLine.transparent = ##f"
    command = _indicators.LilyPondLiteral(string, site="after")
    last_leaf = _select.leaf(score, -1)
    _bind.attach(command, last_leaf)
    lilypond_file = _lilypondfile.LilyPondFile([preamble, score])
    return lilypond_file


def _illustrate_timespan(timespan):
    timespans = _timespan.TimespanList([timespan])
    return _illustrate_markup_maker(timespans)


_class_to_method = dict(
    [
        (_score.Component, _illustrate_component),
        (_indicators.Markup, _illustrate_markup),
        (_metricmodulation.MetricModulation, _illustrate_metric_modulation),
        (_pcollections.PitchClassSegment, _illustrate_pitch_class_segment),
        (_pcollections.PitchSegment, _illustrate_pitch_segment),
        (_pcollections.PitchSet, _illustrate_pitch_set),
        (_timespan.OffsetCounter, _illustrate_markup_maker),
        (_pcollections.PitchRange, _illustrate_pitch_range),
        (_timespan.Timespan, _illustrate_timespan),
        (_timespan.TimespanList, _illustrate_markup_maker),
    ]
)


def attach_markup_struts(lilypond_file):
    """
    LilyPond workaround.

    LilyPond's multisystem cropping currently removes intersystem whitespace.

    These transparent markup struts force LilyPond's cropping to preserve whitespace.
    """
    rhythmic_staff = lilypond_file[_score.Score][-1]
    first_leaf = _get.leaf(rhythmic_staff, 0)
    markup = _indicators.Markup(r"\markup I", direction=_enums.UP)
    _bind.attach(markup, first_leaf)
    _overrides.tweaks(markup, r"- \tweak staff-padding 11")
    _overrides.tweaks(markup, r"- \tweak transparent ##t")
    duration = _get.duration(rhythmic_staff)
    if _duration.Duration(6, 4) < duration:
        last_leaf = _get.leaf(rhythmic_staff, -1)
        markup = _indicators.Markup(r"\markup I", direction=_enums.UP)
        _bind.attach(markup, last_leaf)
        _overrides.tweaks(markup, r"- \tweak staff-padding 18")
        _overrides.tweaks(markup, r"- \tweak transparent ##t")


def components(
    components: typing.Sequence[_score.Component],
    time_signatures: typing.Sequence[_indicators.TimeSignature] | None = None,
    *,
    includes: typing.Sequence[str] | None = None,
):
    """
    Wraps ``components`` in LilyPond file for doc examples.

    Sets LilyPond ``proportionalSpacingDuration`` to 1/24.
    """
    time_signatures = time_signatures or []
    assert all(isinstance(_, _indicators.TimeSignature) for _ in time_signatures), repr(
        time_signatures
    )
    voice = _score.Voice(components, name="Voice")
    staff = _score.Staff([voice], name="Staff")
    score = _score.Score([staff], name="Score", simultaneous=False)
    if not time_signatures:
        duration = _get.duration(components)
        time_signature = _indicators.TimeSignature(duration.pair)
        _bind.attach(time_signature, _select.leaf(components, 0))
    else:
        leaves = _select.leaves(components, grace=False)
        durations = [_.duration for _ in time_signatures]
        parts = _select.partition_by_durations(leaves, durations)
        assert len(parts) == len(time_signatures)
        previous_time_signature = None
        for time_signature, part in zip(time_signatures, parts):
            assert isinstance(time_signature, _indicators.TimeSignature)
            if time_signature != previous_time_signature:
                _bind.attach(time_signature, _select.leaf(part, 0))
            previous_time_signature = time_signature
    items: list[_score.Component | str] = []
    items.append(r'\include "abjad.ily"')
    for include in includes or []:
        items.append(rf'\include "{include}"')
    string = r"""\layout
{
    \context
    {
        \Score
        proportionalNotationDuration = \musicLength 1*1/24
    }
}
"""
    items.append(string)
    items.append(score)
    lilypond_file = _lilypondfile.LilyPondFile(items)
    return lilypond_file


def components_to_score_markup_string(components: typing.Sequence[_score.Component]):
    """
    Changes ``components`` to score markup string.
    """
    assert all(isinstance(_, _score.Component) for _ in components), repr(components)
    components = copy.deepcopy(components)
    staff = _score.Staff(components, name="Rhythmic_Staff")
    staff.lilypond_type = "RhythmicStaff"
    staff.remove_commands.append("Time_signature_engraver")
    staff.remove_commands.append("Staff_symbol_engraver")
    _overrides.override(staff).Stem.direction = _enums.UP
    _overrides.override(staff).Stem.length = 5
    _overrides.override(staff).TupletBracket.bracket_visibility = True
    _overrides.override(staff).TupletBracket.direction = _enums.UP
    _overrides.override(staff).TupletBracket.minimum_length = 4
    _overrides.override(staff).TupletBracket.padding = 1.25
    _overrides.override(staff).TupletBracket.shorten_pair = "#'(-1 . -1.5)"
    scheme = "#ly:spanner::set-spacing-rods"
    _overrides.override(staff).TupletBracket.springs_and_rods = scheme
    _overrides.override(staff).TupletNumber.font_size = 0
    scheme = "#tuplet-number::calc-fraction-text"
    _overrides.override(staff).TupletNumber.text = scheme
    _overrides.setting(staff).tupletFullLength = True
    layout_block = _lilypondfile.Block("layout")
    layout_block.items.append("indent = 0")
    layout_block.items.append("ragged-right = ##t")
    score = _score.Score([staff], name="Score")
    _overrides.override(score).SpacingSpanner.spacing_increment = 0.5
    _overrides.setting(score).proportionalNotationDuration = False
    indent = 4 * " "
    strings = [r"\score", indent + "{"]
    strings.extend([2 * indent + _ for _ in lilypond(score).split("\n")])
    strings.extend([2 * indent + _ for _ in lilypond(layout_block).split("\n")])
    strings.append(indent + "}")
    string = "\n".join(strings)
    return string


def illustrate(item, **keywords):
    """
    Illustrates ``item``.
    """
    method = None
    for key in _class_to_method:
        if isinstance(item, key):
            method = _class_to_method[key]
            break
    if method is None:
        raise Exception(f"can not illustrate objects of type {type(item)}.")
    return method(item, **keywords)


def lilypond(argument, *, site_comments=False, tags=False):
    """
    Gets LilyPond format of ``argument``.
    """
    if not hasattr(argument, "_get_lilypond_format"):
        raise Exception(f"no LilyPond format defined for {argument!r}.")
    string = argument._get_lilypond_format()
    if site_comments is False:
        string = _format.remove_site_comments(string)
    if tags is False:
        string = _tag.remove_tags(string)
    return string


def make_piano_score(leaves=None, lowest_treble_pitch="B3"):
    r"""
    Makes piano score from ``leaves``.

    ..  container:: example

        REGRESSION. Function preserves tweaks:

        >>> note = abjad.Note("c'4")
        >>> abjad.tweak(note.note_head, r"\tweak color #red")
        >>> score = abjad.illustrators.make_piano_score([note])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs:::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            \tweak color #red
                            c'4
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            r4
                        }
                    }
                >>
            >>

        >>> chord = abjad.Chord("<c d a' bf'>4")
        >>> abjad.tweak(chord.note_heads[0], r"\tweak color #red")
        >>> abjad.tweak(chord.note_heads[1], r"\tweak color #red")
        >>> abjad.tweak(chord.note_heads[2], r"\tweak color #blue")
        >>> abjad.tweak(chord.note_heads[3], r"\tweak color #blue")
        >>> score = abjad.illustrators.make_piano_score([chord])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs:::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            <
                                \tweak color #blue
                                a'
                                \tweak color #blue
                                bf'
                            >4
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            <
                                \tweak color #red
                                c
                                \tweak color #red
                                d
                            >4
                        }
                    }
                >>
            >>

    ..  container:: example

        REGRESSION. Function preserves markup:

        >>> note = abjad.Chord("<c bf'>4")
        >>> markup = abjad.Markup(r"\markup loco")
        >>> abjad.attach(markup, chord, direction=abjad.UP)
        >>> markup = abjad.Markup(r"\markup ped.")
        >>> abjad.attach(markup, chord, direction=abjad.DOWN)
        >>> score = abjad.illustrators.make_piano_score([chord])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs:::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            <
                                \tweak color #blue
                                a'
                                \tweak color #blue
                                bf'
                            >4
                            ^ \markup loco
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            <
                                \tweak color #red
                                c
                                \tweak color #red
                                d
                            >4
                            _ \markup ped.
                        }
                    }
                >>
            >>

    """
    leaves = leaves or []
    lowest_treble_pitch = _pitch.NamedPitch(lowest_treble_pitch)
    treble_voice = _score.Voice(name="Treble_Voice")
    treble_staff = _score.Staff([treble_voice], name="Treble_Staff")
    bass_voice = _score.Voice(name="Bass_Voice")
    bass_staff = _score.Staff([bass_voice], name="Bass_Staff")
    staff_group = _score.StaffGroup(
        [treble_staff, bass_staff],
        lilypond_type="PianoStaff",
        name="Piano_Staff",
    )
    score = _score.Score([staff_group], name="Score")
    for leaf in leaves:
        markup_wrappers = _get.indicators(leaf, _indicators.Markup, unwrap=False)
        written_duration = leaf.written_duration
        if isinstance(leaf, _score.Note):
            if leaf.written_pitch < lowest_treble_pitch:
                treble_leaf = _score.Rest(written_duration)
                bass_leaf = copy.copy(leaf)
            else:
                treble_leaf = copy.copy(leaf)
                bass_leaf = _score.Rest(written_duration)
        elif isinstance(leaf, _score.Chord):
            treble_note_heads, bass_note_heads = [], []
            for note_head in leaf.note_heads:
                new_note_head = copy.copy(note_head)
                if new_note_head.written_pitch < lowest_treble_pitch:
                    bass_note_heads.append(new_note_head)
                else:
                    treble_note_heads.append(new_note_head)
            if not treble_note_heads:
                treble_leaf = _score.Rest(written_duration)
            elif len(treble_note_heads) == 1:
                treble_leaf = _score.Note(treble_note_heads[0], written_duration)
            else:
                treble_leaf = _score.Chord(treble_note_heads, written_duration)
            if not bass_note_heads:
                bass_leaf = _score.Rest(written_duration)
            elif len(bass_note_heads) == 1:
                bass_leaf = _score.Note(bass_note_heads[0], written_duration)
            else:
                bass_leaf = _score.Chord(bass_note_heads, written_duration)
        else:
            treble_leaf = copy.copy(leaf)
            bass_leaf = copy.copy(leaf)
        for wrapper in markup_wrappers:
            markup = wrapper.unbundle_indicator()
            markup_copy = copy.copy(markup)
            if wrapper.direction in (_enums.UP, None):
                _bind.attach(markup_copy, treble_leaf, direction=wrapper.direction)
            else:
                _bind.attach(markup_copy, bass_leaf, direction=wrapper.direction)
        treble_voice.append(treble_leaf)
        bass_voice.append(bass_leaf)
    if 0 < len(treble_voice):
        clef = _indicators.Clef("treble")
        _bind.attach(clef, treble_voice[0])
    if 0 < len(bass_voice):
        clef = _indicators.Clef("bass")
        _bind.attach(clef, bass_voice[0])
    return score
