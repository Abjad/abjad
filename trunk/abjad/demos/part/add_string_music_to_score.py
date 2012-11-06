import copy

from abjad.tools import chordtools
from abjad.tools import componenttools
from abjad.tools import iterationtools
from abjad.tools import marktools
from abjad.tools import measuretools
from abjad.tools import notetools
from abjad.tools import resttools
from abjad.tools import tietools

from abjad.demos.part.create_pitch_contour_reservoir import create_pitch_contour_reservoir
from abjad.demos.part.durate_pitch_contour_reservoir import durate_pitch_contour_reservoir
from abjad.demos.part.shadow_pitch_contour_reservoir import shadow_pitch_contour_reservoir
from abjad.demos.part.apply_first_violin_edits import apply_first_violin_edits
from abjad.demos.part.apply_second_violin_edits import apply_second_violin_edits
from abjad.demos.part.apply_viola_edits import apply_viola_edits
from abjad.demos.part.apply_cello_edits import apply_cello_edits
from abjad.demos.part.apply_bass_edits import apply_bass_edits



def add_string_music_to_score(score):

    # generate some pitch and rhythm information
    pitch_contour_reservoir = create_pitch_contour_reservoir()
    shadowed_contour_reservoir = shadow_pitch_contour_reservoir(
        pitch_contour_reservoir)
    durated_reservoir = durate_pitch_contour_reservoir(
        shadowed_contour_reservoir)

    # add six dotted-whole notes and the durated contours to each string voice
    for instrument_name, descents in durated_reservoir.iteritems():
        instrument_voice = score['%s Voice' % instrument_name]
        instrument_voice.extend("R1. R1. R1. R1. R1. R1.")
        for descent in descents:
            instrument_voice.extend(descent)

    # apply instrument-specific edits
    apply_first_violin_edits(score, durated_reservoir)
    apply_second_violin_edits(score, durated_reservoir)
    apply_viola_edits(score, durated_reservoir)
    apply_cello_edits(score, durated_reservoir)
    apply_bass_edits(score, durated_reservoir)

    # chop all string parts into 6/4 measures
    for voice in iterationtools.iterate_voices_in_expr(score['Strings Staff Group']):
        for shard in componenttools.split_components_at_offsets(voice[:],
            [(6, 4)], cyclic=True):
            measuretools.Measure((6, 4), shard)
