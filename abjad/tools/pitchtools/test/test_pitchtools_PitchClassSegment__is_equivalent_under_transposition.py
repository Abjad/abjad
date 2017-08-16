import abjad


def test_pitchtools_PitchClassSegment__is_equivalent_under_transposition_01():

    pitch_class_segment_1 = abjad.PitchClassSegment(['c', 'e', 'b'])
    pitch_class_segment_2 = abjad.PitchClassSegment(['f', 'a', 'e'])
    pitch_class_segment_3 = abjad.PitchClassSegment(['f', 'a'])

    assert pitch_class_segment_1._is_equivalent_under_transposition(
        pitch_class_segment_1)
    assert pitch_class_segment_1._is_equivalent_under_transposition(
        pitch_class_segment_2)
    assert not pitch_class_segment_1._is_equivalent_under_transposition(
        pitch_class_segment_3)

    assert pitch_class_segment_2._is_equivalent_under_transposition(
        pitch_class_segment_1)
    assert pitch_class_segment_2._is_equivalent_under_transposition(
        pitch_class_segment_2)
    assert not pitch_class_segment_2._is_equivalent_under_transposition(
        pitch_class_segment_3)

    assert not pitch_class_segment_3._is_equivalent_under_transposition(
        pitch_class_segment_1)
    assert not pitch_class_segment_3._is_equivalent_under_transposition(
        pitch_class_segment_2)
    assert pitch_class_segment_3._is_equivalent_under_transposition(
        pitch_class_segment_3)
