from abjad import *
from abjad.tools import layouttools
import copy


def make_illustration_from_output_material(markup_inventory, **kwargs):

    notes = []
    for markup in markup_inventory:
        note = Note("c'1")
        markup_copy = markuptools.Markup(markup)
        markup_copy(note)
        marktools.LilyPondCommandMark('break')(note)
        notes.append(note)

    staff = stafftools.RhythmicStaff(notes)
    score = Score([staff])
    illustration = lilypondfiletools.make_basic_lilypond_file(score)
    illustration.layout_block.indent = 0
    illustration.layout_block.ragged_right = True
    illustration.paper_block.top_system_spacing = layouttools.make_spacing_vector(0, 0, 6, 0)
    illustration.paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 6, 0)
    illustration.paper_block.markup_system_spacing = layouttools.make_spacing_vector(0, 0, 12, 0)

    score.override.note_head.transparent = True
    score.override.bar_line.transparent = True
    score.override.bar_number.transparent = True
    score.override.clef.transparent = True
    score.override.span_bar.transparent = True
    score.override.staff_symbol.transparent = True
    score.override.stem.transparent = True
    score.override.time_signature.stencil = False
    score.set.proportional_notation_duration = schemetools.SchemeMoment(1, 8)

    if 'title' in kwargs:
        illustration.header_block.title = markuptools.Markup(kwargs.get('title'))
    if 'subtitle' in kwargs:
        illustration.header_block.subtitle = markuptools.Markup(kwargs.get('subtitle'))

    return illustration
