import copy
from abjad.tools import chordtools
from abjad.tools import componenttools
from abjad.tools import iterationtools
from abjad.tools import marktools
from abjad.tools import measuretools
from abjad.tools import notetools
from abjad.tools import resttools
from abjad.tools import tietools


def add_string_music_to_score(score):
    from abjad.demos import part

    # generate some pitch and rhythm information
    pitch_contour_reservoir = part.create_pitch_contour_reservoir()
    shadowed_contour_reservoir = part.shadow_pitch_contour_reservoir(
        pitch_contour_reservoir)
    durated_reservoir = part.durate_pitch_contour_reservoir(
        shadowed_contour_reservoir)

    # add six dotted-whole notes and the durated contours to each string voice
    for instrument_name, descents in durated_reservoir.iteritems():
        instrument_voice = score['%s Voice' % instrument_name]
        instrument_voice.extend("R1. R1. R1. R1. R1. R1.")
        for descent in descents:
            instrument_voice.extend(descent)

    # apply instrument-specific edits
    part.apply_first_violin_edits(score, durated_reservoir)
    part.apply_second_violin_edits(score, durated_reservoir)
    part.apply_viola_edits(score, durated_reservoir)
    part.apply_cello_edits(score, durated_reservoir)
    part.apply_bass_edits(score, durated_reservoir)

    # chop all string parts into 6/4 measures
    for voice in iterationtools.iterate_voices_in_expr(score['Strings Staff Group']):
        for shard in componenttools.split_components_at_offsets(voice[:],
            [(6, 4)], cyclic=True):
            measuretools.Measure((6, 4), shard)
