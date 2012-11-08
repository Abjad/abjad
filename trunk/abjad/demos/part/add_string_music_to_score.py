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
from abjad.demos.part.edit_first_violin_voice import edit_first_violin_voice
from abjad.demos.part.edit_second_violin_voice import edit_second_violin_voice
from abjad.demos.part.edit_viola_voice import edit_viola_voice
from abjad.demos.part.edit_cello_voice import edit_cello_voice
from abjad.demos.part.edit_bass_voice import edit_bass_voice



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
    edit_first_violin_voice(score, durated_reservoir)
    edit_second_violin_voice(score, durated_reservoir)
    edit_viola_voice(score, durated_reservoir)
    edit_cello_voice(score, durated_reservoir)
    edit_bass_voice(score, durated_reservoir)

    # chop all string parts into 6/4 measures
    for voice in iterationtools.iterate_voices_in_expr(score['Strings Staff Group']):
        for shard in componenttools.split_components_at_offsets(voice[:],
            [(6, 4)], cyclic=True):
            measuretools.Measure((6, 4), shard)
