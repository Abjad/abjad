from abjad import *
import py.test


def test_Measure___cmp___01():
    '''Compare measure to itself.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")

    assert measure == measure
    assert not measure != measure

    comparison_string = 'measure <  measure'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'measure <= measure'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'measure >  measure'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'measure >= measure'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Measure___cmp___02():
    '''Compare measures.
    '''

    measure_1 = Measure((3, 8), "c'8 d'8 e'8")
    measure_2 = Measure((3, 8), "c'8 d'8 e'8")

    assert not measure_1 == measure_2
    assert      measure_1 != measure_2

    comparison_string = 'measure_1 <  measure_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'measure_1 <= measure_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'measure_1 >  measure_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'measure_1 >= measure_2'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Measure___cmp___03():
    '''Compare measure to foreign type.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")

    assert not measure == 'foo'
    assert      measure != 'foo'

    comparison_string = "measure <  'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "measure <= 'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "measure >  'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "measure >= 'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
