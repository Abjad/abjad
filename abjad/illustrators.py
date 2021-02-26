import copy

from . import deprecated, enums, overrides, score, select
from . import timespan as _timespan
from .attach import attach
from .duration import Duration
from .indicators.Clef import Clef
from .indicators.StaffChange import StaffChange
from .iterate import Iteration
from .lilypond import lilypond
from .lilypondfile import Block, LilyPondFile
from .makers import NoteMaker
from .markups import Markup, Postscript
from .metricmodulation import MetricModulation
from .new import new
from .ordereddict import OrderedDict
from .pitch.PitchRange import PitchRange
from .pitch.pitches import NamedPitch
from .pitch.segments import PitchClassSegment, PitchSegment
from .pitch.sets import PitchClassSet, PitchSet
from .spanners import glissando


def _illustrate_component(component):
    block = Block(name="score")
    block.items.append(component)
    lilypond_file = LilyPondFile(items=[block])
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
    markup = Markup.postscript(postscript)
    return _illustrate_markup(markup)


def _illustrate_metric_modulation(metric_modulation):
    lilypond_file = LilyPondFile()
    markup = metric_modulation._get_markup()
    lilypond_file.items.append(markup)
    return lilypond_file


def _illustrate_pitch_class_set(set_):
    chord = score.Chord(set_, Duration(1))
    voice = score.Voice([chord])
    staff = score.Staff([voice])
    score_ = score.Score([staff])
    lilypond_file = LilyPondFile(items=[score_])
    return lilypond_file


def _illustrate_pitch_range(pitch_range):
    start_pitch_clef = Clef.from_pitches([pitch_range.start_pitch])
    stop_pitch_clef = Clef.from_pitches([pitch_range.stop_pitch])
    start_note = score.Note(pitch_range.start_pitch, 1)
    stop_note = score.Note(pitch_range.stop_pitch, 1)
    if start_pitch_clef == stop_pitch_clef:
        if start_pitch_clef == Clef("bass"):
            bass_staff = score.Staff()
            attach(Clef("bass"), bass_staff)
            bass_staff.extend([start_note, stop_note])
            bass_leaves = select.Selection(bass_staff).leaves()
            glissando(bass_leaves)
            score_ = score.Score([bass_staff])
        else:
            treble_staff = score.Staff()
            attach(Clef("treble"), treble_staff)
            treble_staff.extend([start_note, stop_note])
            treble_leaves = select.Selection(treble_staff).leaves()
            glissando(treble_leaves)
            score_ = score.Score([treble_staff])
    else:
        result = make_piano_score()
        score_, treble_staff, bass_staff = result
        bass_staff.extend([start_note, stop_note])
        treble_staff.extend("s1 s1")
        bass_leaves = select.Selection(bass_staff).leaves()
        glissando(bass_leaves)
        attach(StaffChange("Treble_Staff"), bass_staff[1])
        attach(Clef("treble"), treble_staff[0])
        attach(Clef("bass"), bass_staff[0])
    for leaf in Iteration(score_).leaves():
        leaf.multiplier = (1, 4)
    overrides.override(score_).BarLine.stencil = False
    overrides.override(score_).SpanBar.stencil = False
    overrides.override(score_).Glissando.thickness = 2
    overrides.override(score_).TimeSignature.stencil = False
    lilypond_file = LilyPondFile(items=[score_])
    return lilypond_file


def _illustrate_pitch_segment(segment):
    named_pitches = [NamedPitch(x) for x in segment]
    maker = NoteMaker()
    notes = maker(named_pitches, [1])
    result = make_piano_score(leaves=notes, sketch=True)
    score_, treble_staff, bass_staff = result
    for leaf in Iteration(score_).leaves():
        leaf.multiplier = (1, 8)
    overrides.override(score_).Rest.transparent = True
    lilypond_file = LilyPondFile(items=[score_])
    return lilypond_file


def _illustrate_pitch_set(set_):
    upper, lower = [], []
    for pitch in set_:
        if pitch < 0:
            lower.append(pitch)
        else:
            upper.append(pitch)
    if upper:
        upper = score.Chord(upper, Duration(1))
    else:
        upper = score.Skip((1, 1))
    if lower:
        lower = score.Chord(lower, Duration(1))
    else:
        lower = score.Skip((1, 1))
    upper_voice = score.Voice([upper])
    upper_staff = score.Staff([upper_voice])
    lower_voice = score.Voice([lower])
    lower_staff = score.Staff([lower_voice])
    staff_group = score.StaffGroup(
        [upper_staff, lower_staff], lilypond_type="PianoStaff"
    )
    score_ = score.Score([staff_group])
    lilypond_file = LilyPondFile(items=[score_])
    return lilypond_file


def _illustrate_pitch_class_segment(
    segment, markup_direction=enums.Up, figure_name=None
):
    notes = []
    for item in segment:
        note = score.Note(item, Duration(1, 8))
        notes.append(note)
    markup = None
    if segment._equivalence_markup:
        markup = segment._equivalence_markup
    if isinstance(figure_name, str):
        figure_name = Markup(figure_name)
    if figure_name is not None:
        markup = figure_name
    if markup is not None:
        direction = markup_direction
        markup = new(markup, direction=direction)
        attach(markup, notes[0])
    voice = score.Voice(notes)
    staff = score.Staff([voice])
    score_ = score.Score([staff])
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
    deprecated.add_final_bar_line(score_)
    string = r"\override Score.BarLine.transparent = ##f"
    command = overrides.LilyPondLiteral(string, "after")
    last_leaf = select.Selection(score_).leaves()[-1]
    attach(command, last_leaf)
    lilypond_file = LilyPondFile(items=[preamble, score_])
    return lilypond_file


def _illustrate_timespan(timespan):
    timespans = _timespan.TimespanList([timespan])
    return _illustrate_markup_maker(timespans)


_class_to_method = OrderedDict(
    [
        (score.Component, _illustrate_component),
        (Markup, _illustrate_markup),
        (MetricModulation, _illustrate_metric_modulation),
        (_timespan.OffsetCounter, _illustrate_markup_maker),
        (Postscript, _illustrate_postscript),
        (PitchRange, _illustrate_pitch_range),
        (PitchClassSet, _illustrate_pitch_class_set),
        (PitchSegment, _illustrate_pitch_segment),
        (PitchClassSegment, _illustrate_pitch_class_segment),
        (PitchSet, _illustrate_pitch_set),
        (_timespan.Timespan, _illustrate_timespan),
        (_timespan.TimespanList, _illustrate_markup_maker),
    ]
)


### PUBLIC FUNCTIONS ###


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


def make_piano_score(leaves=None, lowest_treble_pitch="B3", sketch=False):
    """
    Makes piano score from ``leaves``.
    """
    leaves = leaves or []
    lowest_treble_pitch = NamedPitch(lowest_treble_pitch)
    treble_staff = score.Staff(name="Treble_Staff")
    bass_staff = score.Staff(name="Bass_Staff")
    staff_group = score.StaffGroup(
        [treble_staff, bass_staff], lilypond_type="PianoStaff"
    )
    score_ = score.Score()
    score_.append(staff_group)
    for leaf in leaves:
        treble_pitches, bass_pitches = [], []
        selection = select.Selection(leaf)
        pitch_set = PitchSet.from_selection(selection)
        for pitch in pitch_set:
            if pitch < lowest_treble_pitch:
                bass_pitches.append(pitch)
            else:
                treble_pitches.append(pitch)
        written_duration = leaf.written_duration
        if not treble_pitches:
            treble_leaf = score.Rest(written_duration)
        elif len(treble_pitches) == 1:
            treble_leaf = score.Note(treble_pitches[0], written_duration)
        else:
            treble_leaf = score.Chord(treble_pitches, written_duration)
        treble_staff.append(treble_leaf)
        if not bass_pitches:
            bass_leaf = score.Rest(written_duration)
        elif len(bass_pitches) == 1:
            bass_leaf = score.Note(bass_pitches[0], written_duration)
        else:
            bass_leaf = score.Chord(bass_pitches, written_duration)
        bass_staff.append(bass_leaf)
    if 0 < len(treble_staff):
        attach(Clef("treble"), treble_staff[0])
    if 0 < len(bass_staff):
        attach(Clef("bass"), bass_staff[0])
    if sketch:
        overrides.override(score_).TimeSignature.stencil = False
        overrides.override(score_).BarNumber.transparent = True
        overrides.override(score_).BarLine.stencil = False
        overrides.override(score_).SpanBar.stencil = False
    return score_, treble_staff, bass_staff


def selection_to_score_markup_string(selection):
    """
    Changes ``selection`` to score markup string.
    """
    selection = copy.deepcopy(selection)
    staff = score.Staff(selection)
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
    score_ = score.Score([staff])
    overrides.override(score_).SpacingSpanner.spacing_increment = 0.5
    overrides.setting(score_).proportionalNotationDuration = False
    indent = 4 * " "
    strings = [r"\score", indent + "{"]
    strings.extend([2 * indent + _ for _ in lilypond(score_).split("\n")])
    strings.extend([2 * indent + _ for _ in lilypond(layout_block).split("\n")])
    strings.append(indent + "}")
    string = "\n".join(strings)
    return string
