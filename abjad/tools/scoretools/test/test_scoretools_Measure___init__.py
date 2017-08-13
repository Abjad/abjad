import abjad


def test_scoretools_Measure___init___01():
    r'''Initializes measure from empty input.
    '''

    measure = abjad.Measure()

    assert measure.time_signature == abjad.TimeSignature((4, 4))
    assert not len(measure)
