from abjad import *


def test_pitchtools_list_named_chromatic_pitch_carriers_in_expr_sorted_by_numbered_chromatic_pitch_class_01():
    '''Works on notes.'''

    chord = Chord([-12, -10, -2, 4, 8, 11, 17, 19, 27, 30, 33, 37], (1, 4))
    sorted_pitches = pitchtools.list_named_chromatic_pitch_carriers_in_expr_sorted_by_numbered_chromatic_pitch_class(chord.written_pitches)

    r'''
    [pitchtools.NamedChromaticPitch(c, 3), pitchtools.NamedChromaticPitch(cs, 7), pitchtools.NamedChromaticPitch(d, 3), pitchtools.NamedChromaticPitch(ef, 6), pitchtools.NamedChromaticPitch(e, 4), pitchtools.NamedChromaticPitch(f, 5), pitchtools.NamedChromaticPitch(fs, 6), pitchtools.NamedChromaticPitch(g, 5), pitchtools.NamedChromaticPitch(af, 4), pitchtools.NamedChromaticPitch(a, 6), pitchtools.NamedChromaticPitch(bf, 3), pitchtools.NamedChromaticPitch(b, 4)]
    '''

    sorted_pitch_numbers = [abs(pitch.numbered_chromatic_pitch) for pitch in sorted_pitches]
    sorted_pcs = [pitch.numbered_chromatic_pitch_class for pitch in sorted_pitches]

    assert sorted_pitch_numbers == [
        -12, 37, -10, 27, 4, 17, 30, 19, 8, 33, -2, 11]
    assert sorted_pcs == [
        pitchtools.NumberedChromaticPitchClass(n) for n in 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
