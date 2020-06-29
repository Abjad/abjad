import copy

from . import enums
from .core.Chord import Chord
from .core.LeafMaker import LeafMaker
from .core.Note import Note
from .core.NoteMaker import NoteMaker
from .core.Score import Score
from .core.Skip import Skip
from .core.Staff import Staff
from .core.StaffGroup import StaffGroup
from .core.Voice import Voice
from .duration import Duration
from .indicators.Clef import Clef
from .indicators.LilyPondLiteral import LilyPondLiteral
from .indicators.StaffChange import StaffChange
from .lilypondfile import Block, LilyPondFile
from .markups import Markup, MarkupCommand
from .pitch.PitchRange import PitchRange
from .pitch.pitches import NamedPitch
from .pitch.segments import PitchSegment, Segment
from .pitch.sets import PitchClassSet, PitchSet
from .scheme import Scheme, SchemeMoment
from .spanners import glissando
from .top import attach, iterate, new, override, select, setting
from .utilities.OrderedDict import OrderedDict


def illustrate(item, **keywords):
    """
    Illustrates ``item``.
    """

    method = None
    for key in class_to_method:
        if isinstance(item, key):
            method = class_to_method[key]
            break
    if method is None:
        raise Exception(f"can not illustrate objects of type {type(item)}.")
    return method(item, **keywords)


def _illustrate_pitch_class_set(set_):
    chord = Chord(set_, Duration(1))
    voice = Voice([chord])
    staff = Staff([voice])
    score = Score([staff])
    lilypond_file = LilyPondFile.new(score)
    return lilypond_file


def _illustrate_pitch_range(pitch_range):
    start_pitch_clef = Clef.from_selection(pitch_range.start_pitch)
    stop_pitch_clef = Clef.from_selection(pitch_range.stop_pitch)
    start_note = Note(pitch_range.start_pitch, 1)
    stop_note = Note(pitch_range.stop_pitch, 1)
    if start_pitch_clef == stop_pitch_clef:
        if start_pitch_clef == Clef("bass"):
            bass_staff = Staff()
            attach(Clef("bass"), bass_staff)
            bass_staff.extend([start_note, stop_note])
            bass_leaves = select(bass_staff).leaves()
            glissando(bass_leaves)
            score = Score([bass_staff])
        else:
            treble_staff = Staff()
            attach(Clef("treble"), treble_staff)
            treble_staff.extend([start_note, stop_note])
            treble_leaves = select(treble_staff).leaves()
            glissando(treble_leaves)
            score = Score([treble_staff])
    else:
        result = Score.make_piano_score()
        score, treble_staff, bass_staff = result
        bass_staff.extend([start_note, stop_note])
        treble_staff.extend(Skip(1) * 2)
        bass_leaves = select(bass_staff).leaves()
        glissando(bass_leaves)
        attach(StaffChange(treble_staff), bass_staff[1])
        attach(Clef("treble"), treble_staff[0])
        attach(Clef("bass"), bass_staff[0])
    for leaf in iterate(score).leaves():
        leaf.multiplier = (1, 4)
    override(score).bar_line.stencil = False
    override(score).span_bar.stencil = False
    override(score).glissando.thickness = 2
    override(score).time_signature.stencil = False
    lilypond_file = LilyPondFile.new(score)
    return lilypond_file


def _illustrate_pitch_segment(segment):
    named_pitches = [NamedPitch(x) for x in segment]
    maker = NoteMaker()
    notes = maker(named_pitches, [1])
    result = Score.make_piano_score(leaves=notes, sketch=True)
    score, treble_staff, bass_staff = result
    for leaf in iterate(score).leaves():
        leaf.multiplier = (1, 8)
    override(score).rest.transparent = True
    lilypond_file = LilyPondFile.new(score)
    return lilypond_file


def _illustrate_pitch_set(set_):
    upper, lower = [], []
    for pitch in set_:
        if pitch < 0:
            lower.append(pitch)
        else:
            upper.append(pitch)
    if upper:
        upper = Chord(upper, Duration(1))
    else:
        upper = Skip((1, 1))
    if lower:
        lower = Chord(lower, Duration(1))
    else:
        lower = Skip((1, 1))
    upper_voice = Voice([upper])
    upper_staff = Staff([upper_voice])
    lower_voice = Voice([lower])
    lower_staff = Staff([lower_voice])
    staff_group = StaffGroup([upper_staff, lower_staff], lilypond_type="PianoStaff")
    score = Score([staff_group])
    lilypond_file = LilyPondFile.new(score)
    return lilypond_file


def _illustrate_segment(
    segment, markup_direction=enums.Up, figure_name=None, **keywords
):
    notes = []
    for item in segment:
        note = Note(item, Duration(1, 8))
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
    voice = Voice(notes)
    staff = Staff([voice])
    score = Score([staff])
    score.add_final_bar_line()
    override(score).bar_line.transparent = True
    override(score).bar_number.stencil = False
    override(score).beam.stencil = False
    override(score).flag.stencil = False
    override(score).stem.stencil = False
    override(score).time_signature.stencil = False
    string = r"\override Score.BarLine.transparent = ##f"
    command = LilyPondLiteral(string, "after")
    last_leaf = select(score).leaves()[-1]
    attach(command, last_leaf)
    moment = SchemeMoment((1, 12))
    setting(score).proportional_notation_duration = moment
    lilypond_file = LilyPondFile.new(music=score)
    if "title" in keywords:
        title = keywords.get("title")
        if not isinstance(title, Markup):
            title = Markup(title)
        lilypond_file.header_block.title = title
    if "subtitle" in keywords:
        markup = Markup(keywords.get("subtitle"))
        lilypond_file.header_block.subtitle = markup
    command = LilyPondLiteral(r"\accidentalStyle forget")
    lilypond_file.layout_block.items.append(command)
    lilypond_file.layout_block.indent = 0
    string = "markup-system-spacing.padding = 8"
    command = LilyPondLiteral(string)
    lilypond_file.paper_block.items.append(command)
    string = "system-system-spacing.padding = 10"
    command = LilyPondLiteral(string)
    lilypond_file.paper_block.items.append(command)
    string = "top-markup-spacing.padding = 4"
    command = LilyPondLiteral(string)
    lilypond_file.paper_block.items.append(command)
    return lilypond_file


class_to_method = OrderedDict(
    [
        (PitchRange, _illustrate_pitch_range),
        (PitchClassSet, _illustrate_pitch_class_set),
        (PitchSegment, _illustrate_pitch_segment),
        (Segment, _illustrate_segment),
        (PitchSet, _illustrate_pitch_set),
    ]
)


def _make_markup_score_block(selection):
    selection = copy.deepcopy(selection)
    staff = Staff(selection)
    staff.lilypond_type = "RhythmicStaff"
    staff.remove_commands.append("Time_signature_engraver")
    staff.remove_commands.append("Staff_symbol_engraver")
    override(staff).stem.direction = enums.Up
    override(staff).stem.length = 5
    override(staff).tuplet_bracket.bracket_visibility = True
    override(staff).tuplet_bracket.direction = enums.Up
    override(staff).tuplet_bracket.minimum_length = 4
    override(staff).tuplet_bracket.padding = 1.25
    override(staff).tuplet_bracket.shorten_pair = (-1, -1.5)
    scheme = Scheme("ly:spanner::set-spacing-rods")
    override(staff).tuplet_bracket.springs_and_rods = scheme
    override(staff).tuplet_number.font_size = 0
    scheme = Scheme("tuplet-number::calc-fraction-text")
    override(staff).tuplet_number.text = scheme
    setting(staff).tuplet_full_length = True
    layout_block = Block(name="layout")
    layout_block.indent = 0
    layout_block.ragged_right = True
    score = Score([staff])
    override(score).spacing_spanner.spacing_increment = 0.5
    setting(score).proportional_notation_duration = False
    return score, layout_block


def _to_score_markup(selection):
    staff, layout_block = _make_markup_score_block(selection)
    command = MarkupCommand("score", [staff, layout_block])
    markup = Markup(command)
    return markup


def duration_to_score_markup(duration):
    maker = LeafMaker()
    notes = maker([0], [duration])
    markup = _to_score_markup(notes)
    return markup
