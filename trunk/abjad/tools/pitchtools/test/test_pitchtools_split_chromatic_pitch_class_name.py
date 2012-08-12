from abjad import *


def test_pitchtools_split_chromatic_pitch_class_name_01():

    assert pitchtools.split_chromatic_pitch_class_name('c') == ('c', '')
    assert pitchtools.split_chromatic_pitch_class_name('cs') == ('c', 's')
    assert pitchtools.split_chromatic_pitch_class_name('d') == ('d', '')
    assert pitchtools.split_chromatic_pitch_class_name('ds') == ('d', 's')
