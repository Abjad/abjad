import abjad
import copy


def add_string_music_to_score(score):
    r'''Adds string music to score.
    '''

    # generate some pitch and rhythm information
    pitch_contour_reservoir = \
        abjad.demos.part.create_pitch_contour_reservoir()
    shadowed_contour_reservoir = \
        abjad.demos.part.shadow_pitch_contour_reservoir(
        pitch_contour_reservoir)
    durated_reservoir = abjad.demos.part.durate_pitch_contour_reservoir(
        shadowed_contour_reservoir)

    # add six dotted-whole notes and the durated contours to each string voice
    for name, descents in durated_reservoir.items():
        instrument_voice = score['%s Voice' % name]
        instrument_voice.extend("R1. R1. R1. R1. R1. R1.")
        for descent in descents:
            instrument_voice.extend(descent)

    # apply instrument-specific edits
    abjad.demos.part.edit_first_violin_voice(score, durated_reservoir)
    abjad.demos.part.edit_second_violin_voice(score, durated_reservoir)
    abjad.demos.part.edit_viola_voice(score, durated_reservoir)
    abjad.demos.part.edit_cello_voice(score, durated_reservoir)
    abjad.demos.part.edit_bass_voice(score, durated_reservoir)

    # chop all string parts into 6/4 measures
    strings_staff_group = score['Strings Staff Group']
    with abjad.ForbidUpdate(score):
        for voice in  abjad.iterate(strings_staff_group).components(abjad.Voice):
            shards = abjad.mutate(voice[:]).split([(6, 4)], cyclic=True)
            for shard in shards:
                measure = abjad.Measure((6, 4), [])
                abjad.mutate(shard).wrap(measure)
