from abjad.tools.pitchtools.Accidental import Accidental
from abjad.tools.pitchtools.NamedDiatonicPitchClass import NamedDiatonicPitchClass
from abjad.tools.pitchtools.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.octave_number_to_octave_tick_string import octave_number_to_octave_tick_string


def _lilypond_enharmonic_transpose(pitch_a, pitch_b, pitch_c):
    if not isinstance(pitch_a, NamedChromaticPitch):
        pitch_a = NamedChromaticPitch(pitch_a)
    if not isinstance(pitch_b, NamedChromaticPitch):
        pitch_b = NamedChromaticPitch(pitch_b)
    if not isinstance(pitch_c, NamedChromaticPitch):
        pitch_c = NamedChromaticPitch(pitch_c)

    scale = [0., 2., 4., 5., 7., 9., 11.]

    def step_size(step):
        normalized_step = step % len(scale)
        if normalized_step == 6:
            return 1. # b to c
        return scale[normalized_step + 1] - scale[normalized_step]

    def normalize_alteration(step, alteration):
        while 2. < alteration:
            alteration -= step_size(step)
            step += 1.
        while alteration < -2.:
            step -= 1.
            alteration += step_size(step)
        return step, alteration

    def normalize_octave(octave, step):
        normalized_step = step % len(scale)
        octave += (step - normalized_step) / len(scale)
        return octave, normalized_step

    a_oct, a_step, a_alt = pitch_a.octave_number, pitch_a.diatonic_pitch_class_number, pitch_a._accidental.semitones
    b_oct, b_step, b_alt = pitch_b.octave_number, pitch_b.diatonic_pitch_class_number, pitch_b._accidental.semitones
    c_oct, c_step, c_alt = pitch_c.octave_number, pitch_c.diatonic_pitch_class_number, pitch_c._accidental.semitones

    d_oct, d_step, d_alt, d_tones = b_oct - a_oct, b_step - a_step, b_alt - a_alt, float(pitch_b) - float(pitch_a)

    tmp_alt = float(pitch_c) + d_tones

    # print 'TMP_ALT: %f' % tmp_alt

    new_oct = c_oct + d_oct
    new_step = c_step + d_step
    new_alt = c_alt

    # print 'NEW:', new_oct, new_step, new_alt

    new_step, new_alt = normalize_alteration(new_step, new_alt)
    new_oct, new_step = normalize_octave(new_oct, new_step)

    # print 'NEW(norm):', new_oct, new_step, new_alt

    octave_ticks = octave_number_to_octave_tick_string(new_oct)
    pitch_class_name = str(NamedDiatonicPitchClass(int(new_step)))
    accidental = str(Accidental(new_alt))

    tmp_pitch = NamedChromaticPitch(pitch_class_name + accidental + octave_ticks)

    # print 'TMP(pitch): %r' % tmp_pitch

    new_alt += tmp_alt - float(tmp_pitch)

    # print 'NEW(alt): %f' % new_alt

    new_step, new_alt = normalize_alteration(new_step, new_alt)
    new_oct, new_step = normalize_octave(new_oct, new_step)
    
    # print 'NEW(norm):', new_oct, new_step, new_alt

    octave_ticks = octave_number_to_octave_tick_string(new_oct)
    pitch_class_name = str(NamedDiatonicPitchClass(int(new_step)))
    accidental = str(Accidental(new_alt))

    return NamedChromaticPitch(pitch_class_name + accidental + octave_ticks)
