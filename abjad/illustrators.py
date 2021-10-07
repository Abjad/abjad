import copy

from . import deprecated, enums, get
from . import iterate as iterate_
from . import markups as _markups
from . import overrides
from . import score as _score
from . import selection as _selection
from . import timespan as _timespan
from .bind import attach
from .duration import Duration
from .indicators.Clef import Clef
from .indicators.StaffChange import StaffChange
from .indicators.TimeSignature import TimeSignature
from .lilypondfile import Block, LilyPondFile
from .lilypondformat import lilypond
from .makers import NoteMaker
from .metricmodulation import MetricModulation
from .new import new
from .pitch.PitchRange import PitchRange
from .pitch.pitches import NamedPitch
from .pitch.segments import PitchClassSegment, PitchSegment
from .pitch.sets import PitchClassSet, PitchSet
from .spanners import glissando


def _illustrate_component(component):
    block = Block(name="score")
    block.items.append(component)
    lilypond_file = LilyPondFile([block])
    return lilypond_file


def _illustrate_markup(markup):
    lilypond_file = LilyPondFile()
    markup = new(markup, direction=None)
    lilypond_file.items.append(markup)
    return lilypond_file


def _illustrate_markup_maker(argument, **keywords):
    markup = argument._make_markup(**keywords)
    return _illustrate_markup(markup)


def _illustrate_postscript(postscript):
    if isinstance(postscript, _markups.Postscript):
        postscript = str(postscript)
    assert isinstance(postscript, str)
    string = "\n".join([r"\markup", r"\postscript", '#"', postscript, '"'])
    markup = _markups.Markup(string, literal=True)
    return _illustrate_markup(markup)


def _illustrate_metric_modulation(metric_modulation):
    lilypond_file = LilyPondFile()
    markup = metric_modulation._get_markup()
    lilypond_file.items.append(markup)
    return lilypond_file


def _illustrate_pitch_class_set(set_):
    chord = _score.Chord(set_, Duration(1))
    voice = _score.Voice([chord], name="Voice")
    staff = _score.Staff([voice], name="Staff")
    score = _score.Score([staff], name="Score")
    lilypond_file = LilyPondFile([score])
    return lilypond_file


def _illustrate_pitch_range(pitch_range):
    start_pitch_clef = Clef.from_pitches([pitch_range.start_pitch])
    stop_pitch_clef = Clef.from_pitches([pitch_range.stop_pitch])
    start_note = _score.Note(pitch_range.start_pitch, 1)
    stop_note = _score.Note(pitch_range.stop_pitch, 1)
    if start_pitch_clef == stop_pitch_clef:
        if start_pitch_clef == Clef("bass"):
            bass_staff = _score.Staff(name="Bass_Staff")
            attach(Clef("bass"), bass_staff)
            bass_staff.extend([start_note, stop_note])
            bass_leaves = _selection.Selection(bass_staff).leaves()
            glissando(bass_leaves)
            score = _score.Score([bass_staff], name="Score")
        else:
            treble_staff = _score.Staff(name="Treble_Staff")
            attach(Clef("treble"), treble_staff)
            treble_staff.extend([start_note, stop_note])
            treble_leaves = _selection.Selection(treble_staff).leaves()
            glissando(treble_leaves)
            score = _score.Score([treble_staff], name="Score")
    else:
        score = make_piano_score()
        treble_staff, bass_staff = score["Treble_Staff"], score["Bass_Staff"]
        bass_staff.extend([start_note, stop_note])
        treble_staff.extend("s1 s1")
        bass_leaves = _selection.Selection(bass_staff).leaves()
        glissando(bass_leaves)
        attach(StaffChange("Treble_Staff"), bass_staff[1])
        attach(Clef("treble"), treble_staff[0])
        attach(Clef("bass"), bass_staff[0])
    for leaf in iterate_.leaves(score):
        leaf.multiplier = (1, 4)
    overrides.override(score).BarLine.stencil = False
    overrides.override(score).SpanBar.stencil = False
    overrides.override(score).Glissando.thickness = 2
    overrides.override(score).TimeSignature.stencil = False
    lilypond_file = LilyPondFile([score])
    return lilypond_file


def _illustrate_pitch_segment(segment):
    named_pitches = [NamedPitch(x) for x in segment]
    maker = NoteMaker()
    notes = maker(named_pitches, [1])
    score = make_piano_score(leaves=notes)
    overrides.override(score).TimeSignature.stencil = False
    overrides.override(score).BarLine.stencil = False
    overrides.override(score).SpanBar.stencil = False
    for leaf in iterate_.leaves(score):
        leaf.multiplier = (1, 8)
    overrides.override(score).Rest.transparent = True
    lilypond_file = LilyPondFile([score])
    return lilypond_file


def _illustrate_pitch_set(set_):
    upper, lower = [], []
    for pitch in set_:
        if pitch < 0:
            lower.append(pitch)
        else:
            upper.append(pitch)
    if upper:
        upper = _score.Chord(upper, Duration(1))
    else:
        upper = _score.Skip((1, 1))
    if lower:
        lower = _score.Chord(lower, Duration(1))
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
    lilypond_file = LilyPondFile([score])
    return lilypond_file


def _illustrate_pitch_class_segment(
    segment, markup_direction=enums.Up, figure_name=None
):
    notes = []
    for item in segment:
        note = _score.Note(item, Duration(1, 8))
        notes.append(note)
    markup = None
    if isinstance(figure_name, str):
        figure_name = _markups.Markup(rf"\markup {figure_name}", literal=True)
    if figure_name is not None:
        markup = figure_name
    if markup is not None:
        direction = markup_direction
        markup = new(markup, direction=direction)
        attach(markup, notes[0])
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
        proportionalNotationDuration = #(ly:make-moment 1 12)
    }
}

\paper {
    markup-system-spacing.padding = 8
    system-system-spacing.padding = 10
    top-markup-spacing.padding = 4
}"""
    deprecated.add_final_bar_line(score)
    string = r"\override Score.BarLine.transparent = ##f"
    command = overrides.LilyPondLiteral(string, "after")
    last_leaf = _selection.Selection(score).leaves()[-1]
    attach(command, last_leaf)
    lilypond_file = LilyPondFile([preamble, score])
    return lilypond_file


def _illustrate_timespan(timespan):
    timespans = _timespan.TimespanList([timespan])
    return _illustrate_markup_maker(timespans)


_class_to_method = dict(
    [
        (_score.Component, _illustrate_component),
        (_markups.Markup, _illustrate_markup),
        (MetricModulation, _illustrate_metric_modulation),
        (_timespan.OffsetCounter, _illustrate_markup_maker),
        (_markups.Postscript, _illustrate_postscript),
        (PitchRange, _illustrate_pitch_range),
        (PitchClassSet, _illustrate_pitch_class_set),
        (PitchSegment, _illustrate_pitch_segment),
        (PitchClassSegment, _illustrate_pitch_class_segment),
        (PitchSet, _illustrate_pitch_set),
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
    first_leaf = get.leaf(rhythmic_staff, 0)
    markup = _markups.Markup(r"\markup I", direction=enums.Up, literal=True)
    attach(markup, first_leaf)
    overrides.tweak(markup).staff_padding = 11
    overrides.tweak(markup).transparent = "##t"
    duration = get.duration(rhythmic_staff)
    if Duration(6, 4) < duration:
        last_leaf = get.leaf(rhythmic_staff, -1)
        markup = _markups.Markup(r"\markup I", direction=enums.Up, literal=True)
        attach(markup, last_leaf)
        overrides.tweak(markup).staff_padding = 18
        overrides.tweak(markup).transparent = "##t"


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


def make_piano_score(leaves=None, lowest_treble_pitch="B3"):
    r"""
    Makes piano score from ``leaves``.

    ..  container:: example

        REGRESSION. Function preserves tweaks:

        >>> note = abjad.Note("c'4")
        >>> abjad.tweak(note.note_head).color = "red"
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
                        \clef "treble"
                        \tweak color #red
                        c'4
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r4
                    }
                >>
            >>

        >>> chord = abjad.Chord("<c d a' bf'>4")
        >>> abjad.tweak(chord.note_heads[0]).color = "red"
        >>> abjad.tweak(chord.note_heads[1]).color = "red"
        >>> abjad.tweak(chord.note_heads[2]).color = "blue"
        >>> abjad.tweak(chord.note_heads[3]).color = "blue"
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
                        \clef "treble"
                        <
                            \tweak color #blue
                            a'
                            \tweak color #blue
                            bf'
                        >4
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        <
                            \tweak color #red
                            c
                            \tweak color #red
                            d
                        >4
                    }
                >>
            >>

    ..  container:: example

        REGRESSION. Function preserves markup:

        >>> note = abjad.Chord("<c bf'>4")
        >>> markup = abjad.Markup(r"\markup loco", direction=abjad.Up, literal=True)
        >>> abjad.attach(markup, chord)
        >>> markup = abjad.Markup(r"\markup ped.", direction=abjad.Down, literal=True)
        >>> abjad.attach(markup, chord)
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
                        \clef "treble"
                        <
                            \tweak color #blue
                            a'
                            \tweak color #blue
                            bf'
                        >4
                        ^ \markup loco
                    }
                    \context Staff = "Bass_Staff"
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
                >>
            >>

    """
    leaves = leaves or []
    lowest_treble_pitch = NamedPitch(lowest_treble_pitch)
    treble_staff = _score.Staff(name="Treble_Staff")
    bass_staff = _score.Staff(name="Bass_Staff")
    staff_group = _score.StaffGroup(
        [treble_staff, bass_staff],
        lilypond_type="PianoStaff",
        name="Piano_Staff",
    )
    score = _score.Score(name="Score")
    score.append(staff_group)
    for leaf in leaves:
        markups = get.indicators(leaf, _markups.Markup)
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
        for markup in markups:
            markup_copy = copy.copy(markup)
            if markup.direction in (enums.Up, None):
                attach(markup_copy, treble_leaf)
            else:
                attach(markup_copy, bass_leaf)
        treble_staff.append(treble_leaf)
        bass_staff.append(bass_leaf)
    if 0 < len(treble_staff):
        attach(Clef("treble"), treble_staff[0])
    if 0 < len(bass_staff):
        attach(Clef("bass"), bass_staff[0])
    return score


def selection(selection, time_signatures=None, *, includes=None):
    """
    Wraps ``selection`` in LilyPond file for doc examples.
    """
    if time_signatures is None:
        duration = get.duration(selection)
        time_signature = TimeSignature(duration)
        attach(time_signature, _selection.Selection(selection).leaf(0))
    else:
        leaves = _selection.Selection(selection).leaves(grace=False)
        parts = leaves.partition_by_durations(time_signatures)
        assert len(parts) == len(time_signatures)
        for time_signature, part in zip(time_signatures, parts):
            time_signature = TimeSignature(time_signature)
            attach(time_signature, _selection.Selection(part).leaf(0))
    staff = _score.Staff(selection, name="Staff")
    score = _score.Score([staff], name="Score")
    preamble = r"""\include "abjad.ily"

\layout {
    \context {
        \Score
        proportionalNotationDuration = #(ly:make-moment 1 24)
    }
}
"""
    lilypond_file = LilyPondFile([preamble, score], includes=includes)
    return lilypond_file


def selection_to_score_markup_string(selection):
    """
    Changes ``selection`` to score markup string.
    """
    selection = copy.deepcopy(selection)
    staff = _score.Staff(selection, name="Rhythmic_Staff")
    staff.lilypond_type = "RhythmicStaff"
    staff.remove_commands.append("Time_signature_engraver")
    staff.remove_commands.append("Staff_symbol_engraver")
    overrides.override(staff).Stem.direction = enums.Up
    overrides.override(staff).Stem.length = 5
    overrides.override(staff).TupletBracket.bracket_visibility = True
    overrides.override(staff).TupletBracket.direction = enums.Up
    overrides.override(staff).TupletBracket.minimum_length = 4
    overrides.override(staff).TupletBracket.padding = 1.25
    overrides.override(staff).TupletBracket.shorten_pair = "#'(-1 . -1.5)"
    scheme = "#ly:spanner::set-spacing-rods"
    overrides.override(staff).TupletBracket.springs_and_rods = scheme
    overrides.override(staff).TupletNumber.font_size = 0
    scheme = "#tuplet-number::calc-fraction-text"
    overrides.override(staff).TupletNumber.text = scheme
    overrides.setting(staff).tupletFullLength = True
    layout_block = Block(name="layout")
    layout_block.indent = 0
    layout_block.ragged_right = "##t"
    score = _score.Score([staff], name="Score")
    overrides.override(score).SpacingSpanner.spacing_increment = 0.5
    overrides.setting(score).proportionalNotationDuration = False
    indent = 4 * " "
    strings = [r"\score", indent + "{"]
    strings.extend([2 * indent + _ for _ in lilypond(score).split("\n")])
    strings.extend([2 * indent + _ for _ in lilypond(layout_block).split("\n")])
    strings.append(indent + "}")
    string = "\n".join(strings)
    return string
