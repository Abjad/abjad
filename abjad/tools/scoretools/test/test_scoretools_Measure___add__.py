import abjad
import pytest


@pytest.mark.skip()
def test_scoretools_Measure___add___01():
    r'''Add outside-of-score measures.
    '''

    measure_1 = abjad.Measure((1, 8), "c'16 d'16")
    beam = abjad.Beam()
    abjad.attach(beam, measure_1[:])
    measure_2 = abjad.Measure((2, 16), "c'16 d'16")
    slur = abjad.Slur()
    abjad.attach(slur, measure_2[:])
    new = measure_1 + measure_2

    assert format(new) == abjad.String.normalize(
        r'''
        {
            \time 2/8
            c'16 [
            d'16 ]
            c'16 (
            d'16 )
        }
        '''
        )

    assert new is not measure_1 and new is not measure_2
    assert len(measure_1) == 0
    assert len(measure_2) == 0
    assert abjad.inspect(new).is_well_formed()


@pytest.mark.skip()
def test_scoretools_Measure___add___02():
    r'''Add measures in score.
    '''

    measure_1 = abjad.Measure((1, 8), "c'16 d'16")
    beam = abjad.Beam()
    abjad.attach(beam, measure_1[:])
    measure_2 = abjad.Measure((2, 16), "c'16 d'16")
    slur = abjad.Slur()
    abjad.attach(slur, measure_2[:])
    staff = abjad.Staff([measure_1, measure_2])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            {
                \time 1/8
                c'16 [
                d'16 ]
            }
            {
                \time 2/16
                c'16 (
                d'16 )
            }
        }
        '''
        )

    new = measure_1 + measure_2

    assert new is not measure_1 and new is not measure_2
    assert len(measure_1) == 0
    assert len(measure_2) == 0

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'16 [
                d'16 ]
                c'16 (
                d'16 )
            }
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()
