import abjad


def test_scoretools_MultimeasureRest___init___01():
    r'''Initializes multimeasure rest from empty input.
    '''

    multimeasure_rest = abjad.MultimeasureRest()

    assert format(multimeasure_rest) == abjad.String.normalize(
        r'''
        R4
        '''
        )

    assert abjad.inspect(multimeasure_rest).is_well_formed()
