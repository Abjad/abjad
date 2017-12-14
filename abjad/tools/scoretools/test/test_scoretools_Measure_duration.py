import abjad
import pytest


def test_scoretools_Measure_duration_01():
    r'''Properly filled measure with power-of-two time signature.
    '''

    measure = abjad.Measure((3, 8), "c'8 d'8 e'8")

    assert format(measure) == abjad.String.normalize(
        r'''
        { % measure
            \time 3/8
            c'8
            d'8
            e'8
        } % measure
        '''
        )

    assert measure._get_contents_duration() == abjad.Duration(3, 8)
    assert measure._get_preprolated_duration() == abjad.Duration(3, 8)
    assert abjad.inspect(measure).get_duration() == abjad.Duration(3, 8)


def test_scoretools_Measure_duration_02():
    r'''Properly filled measure with non-power-of-two time signature.
    '''

    measure = abjad.Measure((3, 10), "c'8 d'8 e'8")
    measure.implicit_scaling = True

    assert format(measure) == abjad.String.normalize(
        r'''
        { % measure
            \time 3/10
            \scaleDurations #'(4 . 5) {
                c'8
                d'8
                e'8
            }
        } % measure
        '''
        )

    assert measure._get_contents_duration() == abjad.Duration(3, 8)
    assert measure._get_preprolated_duration() == abjad.Duration(3, 10)
    assert abjad.inspect(measure).get_duration() == abjad.Duration(3, 10)


def test_scoretools_Measure_duration_03():
    r'''Improperly filled measure with power-of-two time signature.
    '''

    measure = abjad.Measure((3, 8), "c'8 d'8 e'8 f'8")

    assert pytest.raises(abjad.OverfullContainerError, 'format(measure)')

    assert measure._get_contents_duration() == abjad.Duration(4, 8)
    assert measure._get_preprolated_duration() == abjad.Duration(4, 8)
    assert abjad.inspect(measure).get_duration() == abjad.Duration(4, 8)


def test_scoretools_Measure_duration_04():
    r'''Impropely filled measure with non-power-of-two time signature.
    '''

    measure = abjad.Measure((3, 10), "c'8 d'8 e'8 f'8")
    measure.implicit_scaling = True

    assert pytest.raises(abjad.OverfullContainerError, 'format(measure)')

    assert measure._get_contents_duration() == abjad.Duration(4, 8)
    assert measure._get_preprolated_duration() == abjad.Duration(4, 10)
    assert abjad.inspect(measure).get_duration() == abjad.Duration(4, 10)
