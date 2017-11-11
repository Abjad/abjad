import abjad


def test_scoretools_Measure_time_signature_update_01():
    r'''Measures allow time signature update.
    '''

    measure = abjad.Measure((4, 8), "c'8 d'8 e'8 f'8")
    measure.pop()
    abjad.detach(abjad.TimeSignature, measure)
    time_signature = abjad.TimeSignature((3, 8))
    abjad.attach(time_signature, measure)

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

    assert abjad.inspect(measure).is_well_formed()
