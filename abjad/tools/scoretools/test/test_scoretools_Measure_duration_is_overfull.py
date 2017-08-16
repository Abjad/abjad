import abjad


def test_scoretools_Measure_duration_is_overfull_01():

    measure = abjad.Measure((3, 8), "c'8 c'8 c'8")
    assert not measure.is_overfull

    abjad.detach(abjad.TimeSignature, measure)
    time_signature = abjad.TimeSignature((2, 8))
    abjad.attach(time_signature, measure)
    assert measure.is_overfull

    abjad.detach(abjad.TimeSignature, measure)
    time_signature = abjad.TimeSignature((3, 8))
    abjad.attach(time_signature, measure)
    assert not measure.is_overfull
