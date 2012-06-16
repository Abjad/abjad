from abjad import *


def test_Measure___delitem___01():
    '''Nonnegative indices work.
    
    Automatically update time signature.
    '''

    measure = Measure((4, 8), Note(0, (1, 8)) * 4)
    measure.automatically_adjust_time_signature = True
    del(measure[:1])

    assert componenttools.is_well_formed_component(measure)
    assert measure.lilypond_format == "{\n\t\\time 3/8\n\tc'8\n\tc'8\n\tc'8\n}"


def test_Measure___delitem___02():
    '''Negative indices work.

    Automatically update time signatures.
    '''

    measure = Measure((4, 8), Note(0, (1, 8)) * 4)
    measure.automatically_adjust_time_signature = True
    del(measure[-1:])

    assert componenttools.is_well_formed_component(measure)
    assert measure.lilypond_format == "{\n\t\\time 3/8\n\tc'8\n\tc'8\n\tc'8\n}"


def test_Measure___delitem___03():
    '''Denominator preservation in time signature.

    Automatically update time signature.
    '''

    measure = Measure((4, 8), Note(0, (1, 8)) * 4)
    measure.automatically_adjust_time_signature = True
    del(measure[:2])

    assert componenttools.is_well_formed_component(measure)
    assert measure.lilypond_format == "{\n\t\\time 2/8\n\tc'8\n\tc'8\n}"


def test_Measure___delitem___04():
    '''Denominator changes from 8 to 16.

    Automatically update time signature.
    '''

    measure = Measure((4, 8), Note(0, (1, 16)) * 2 + Note(0, (1, 8)) * 3)
    measure.automatically_adjust_time_signature = True
    del(measure[:1])

    assert componenttools.is_well_formed_component(measure)
    assert measure.lilypond_format == "{\n\t\\time 7/16\n\tc'16\n\tc'8\n\tc'8\n\tc'8\n}"


def test_Measure___delitem___05():
    '''Trim nonbinary measure.

    Automatically update time signature.
    '''

    measure = Measure((4, 9), "c'8 d'8 e'8 f'8")
    measure.automatically_adjust_time_signature = True
    del(measure[:1])

    r'''
    {
        \time 3/9
        \scaleDurations #'(8 . 9) {
            d'8
            e'8
            f'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(measure)
    assert measure.lilypond_format == "{\n\t\\time 3/9\n\t\\scaleDurations #'(8 . 9) {\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n}"


def test_Measure___delitem___06():
    '''Trim nonbinary measure, with denominator change.

    Automatically update time signature.
    '''

    measure = Measure((3, 9), "c'16 d'16 e'8 f'8")
    measure.automatically_adjust_time_signature = True

    r'''
    {
        \time 3/9
        \scaleDurations #'(8 . 9) {
            c'16
            d'16
            e'8
            f'8
        }
    }
    '''

    del(measure[:1])

    r'''
    {
        \time 5/18
        \scaleDurations #'(8 . 9) {
            d'16
            e'8
            f'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(measure)
    assert measure.lilypond_format == "{\n\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\td'16\n\t\te'8\n\t\tf'8\n\t}\n}"


def test_Measure___delitem___07():
    '''Nonnegative indices work.
    
    Do NOT automatically update time signature.
    '''

    measure = Measure((4, 8), "c'8 c' c' c'")
    del(measure[:1])

    assert not componenttools.is_well_formed_component(measure)
    assert len(measure) == 3
    assert contexttools.get_time_signature_mark_attached_to_component(measure) == (4, 8)


def test_Measure___delitem___08():
    '''Nonbinary measure.

    Do NOT automatically update time signature.
    '''
 
    measure = Measure((4, 9), "c'8 d' e' f'")
    del(measure[:1])

    assert not componenttools.is_well_formed_component(measure)
    assert len(measure) == 3
    assert contexttools.get_time_signature_mark_attached_to_component(measure) == (4, 9)
