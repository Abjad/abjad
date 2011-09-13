from abjad import *
import py.test


def test_Score___cmp___01():
    '''Compare score to itself.
    '''

    score = Score([])

    assert score == score
    assert not score != score

    comparison_string = 'score <  score'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'score <= score'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'score >  score'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'score >= score'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Score___cmp___02():
    '''Compare scores.
    '''

    score_1 = Score([])
    score_2 = Score([])

    assert not score_1 == score_2
    assert      score_1 != score_2

    comparison_string = 'score_1 <  score_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'score_1 <= score_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'score_1 >  score_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'score_1 >= score_2'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Score___cmp___03():
    '''Compare score to foreign type.
    '''

    score = Score([])

    assert not score == 'foo'
    assert      score != 'foo'

    comparison_string = "score <  'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "score <= 'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "score >  'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "score >= 'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
