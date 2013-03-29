from abjad import *
from abjad.tools import layouttools
import baca
import os


def make_illustration_from_output_material(output_material, **kwargs):

    chords = []
    for constellation_number, aggregate_number in output_material:
        constellation_index = constellation_number - 1
        aggregate_index = aggregate_number - 1
        pitch_numbers = baca.pitch.CC.get(constellation_number, aggregate_number)
        chord = Chord(pitch_numbers, Duration(1, 1))
        chords.append(chord)

    score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves(chords)
    illustration = lilypondfiletools.make_basic_lilypond_file(score)
    illustration.paper_block.top_system_spacing = layouttools.make_spacing_vector(0, 0, 6, 0)

    stylesheet = os.path.join(os.environ.get('SCFPATH'), 'stylesheets', 'rhythm_letter_16.ly')
    illustration.file_initial_user_includes.append(stylesheet)
    scoretools.add_double_bar_to_end_of_score(score)

    score.override.bar_line.transparent = True
    score.override.rest.transparent = True
    score.override.span_bar.transparent = True
    score.override.time_signature.stencil = False
    score.set.proportional_notation_duration = schemetools.SchemeMoment(1, 4)

    if 'title' in kwargs:
        illustration.header_block.title = markuptools.Markup(kwargs.get('title'))
    if 'subtitle' in kwargs:
        illustration.header_block.subtitle = markuptools.Markup(kwargs.get('subtitle'))

    return illustration
