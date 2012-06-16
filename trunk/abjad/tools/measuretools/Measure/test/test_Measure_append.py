from abjad import *
import py


def test_Measure_append_01():
    '''Time signature does not automatically adjust.
    '''

    measure = Measure((3, 4), "c' d' e'")
    measure.append('r')

    assert measure.is_overfull
    assert py.test.raises(Exception, 'f(measure)')


def test_Measure_append_02():
    '''Time signature adjusts automatically.
    '''

    measure = Measure((3, 4), "c' d' e'")
    measure.automatically_adjust_time_signature = True
    measure.append('r')

    assert not measure.is_misfilled
    assert measure.lilypond_format == "{\n\t\\time 4/4\n\tc'4\n\td'4\n\te'4\n\tr4\n}"
