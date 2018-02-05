import abjad


def test_scoretools_Measure___delitem___01():
    r'''Nonnegative indices work.

    Automatically update time signature.
    '''

    measure = abjad.Measure((4, 8), "c'8 c'8 c'8 c'8")
    measure.automatically_adjust_time_signature = True
    del(measure[:1])

    assert format(measure) == abjad.String.normalize(
        r'''
        {   % measure
            \time 3/8
            c'8
            c'8
            c'8
        }   % measure
        '''
        )

    assert abjad.inspect(measure).is_well_formed()


def test_scoretools_Measure___delitem___02():
    r'''Negative indices work.

    Automatically update time signatures.
    '''

    measure = abjad.Measure((4, 8), "c'8 c'8 c'8 c'8")
    measure.automatically_adjust_time_signature = True
    del(measure[-1:])

    assert format(measure) == abjad.String.normalize(
        r'''
        {   % measure
            \time 3/8
            c'8
            c'8
            c'8
        }   % measure
        '''
        )

    assert abjad.inspect(measure).is_well_formed()


def test_scoretools_Measure___delitem___03():
    r'''Denominator preservation in time signature.

    Automatically update time signature.
    '''

    measure = abjad.Measure((4, 8), "c'8 c'8 c'8 c'8")
    measure.automatically_adjust_time_signature = True
    del(measure[:2])

    assert format(measure) == abjad.String.normalize(
        r'''
        {   % measure
            \time 2/8
            c'8
            c'8
        }   % measure
        '''
        )

    assert abjad.inspect(measure).is_well_formed()


def test_scoretools_Measure___delitem___04():
    r'''Denominator changes from 8 to 16.

    Automatically update time signature.
    '''

    measure = abjad.Measure((4, 8), "c'16 c'16 c'8 c'8 c'8")
    measure.automatically_adjust_time_signature = True
    del(measure[:1])

    assert format(measure) == abjad.String.normalize(
        r'''
        {   % measure
            \time 7/16
            c'16
            c'8
            c'8
            c'8
        }   % measure
        '''
        )

    assert abjad.inspect(measure).is_well_formed()


def test_scoretools_Measure___delitem___05():
    r'''Trim non-power-of-two measure.

    Automatically update time signature.
    '''

    measure = abjad.Measure((4, 9), "c'8 d'8 e'8 f'8")
    measure.implicit_scaling = True
    measure.automatically_adjust_time_signature = True
    del(measure[:1])

    assert format(measure) == abjad.String.normalize(
        r'''
        {   % measure
            \time 3/9
            \scaleDurations #'(8 . 9) {
                d'8
                e'8
                f'8
            }
        }   % measure
        '''
        )

    assert abjad.inspect(measure).is_well_formed()


def test_scoretools_Measure___delitem___06():
    r'''Trim non-power-of-two measure, with denominator change.

    Automatically update time signature.
    '''

    measure = abjad.Measure((3, 9), "c'16 d'16 e'8 f'8")
    measure.implicit_scaling = True
    measure.automatically_adjust_time_signature = True

    assert format(measure) == abjad.String.normalize(
        r'''
        {   % measure
            \time 3/9
            \scaleDurations #'(8 . 9) {
                c'16
                d'16
                e'8
                f'8
            }
        }   % measure
        '''
        )

    del(measure[:1])

    assert format(measure) == abjad.String.normalize(
        r'''
        {   % measure
            \time 5/18
            \scaleDurations #'(8 . 9) {
                d'16
                e'8
                f'8
            }
        }   % measure
        '''
        )

    assert abjad.inspect(measure).is_well_formed()


def test_scoretools_Measure___delitem___07():
    r'''Nonnegative indices work.

    Do NOT automatically update time signature.
    '''

    measure = abjad.Measure((4, 8), "c'8 c' c' c'")
    del(measure[:1])

    assert len(measure) == 3
    assert abjad.inspect(measure).get_indicator(abjad.TimeSignature)
    assert not abjad.inspect(measure).is_well_formed()


def test_scoretools_Measure___delitem___08():
    r'''Non-power-of-two measure.

    Do NOT automatically update time signature.
    '''

    measure = abjad.Measure((4, 9), "c'8 d' e' f'")
    measure.implicit_scaling = True
    del(measure[:1])

    assert len(measure) == 3
    assert abjad.inspect(measure).get_indicator(abjad.TimeSignature)
    assert not abjad.inspect(measure).is_well_formed()
