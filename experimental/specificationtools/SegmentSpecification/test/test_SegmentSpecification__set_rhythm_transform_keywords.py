import py
from abjad import *
from experimental import *


def test_SegmentSpecification__set_rhythm_transform_keywords_01():
    '''Rhythm 'index' keyword.
    '''
    py.test.skip('implement eventually')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.make_segment('red')
    red_segment.set_time_signatures([(3, 8), (4, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.dotted_sixteenths, index=1)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__set_rhythm_transform_keywords_02():
    '''Rhythm 'count' keyword.
    '''
    py.test.skip('implement eventually')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.make_segment('red')
    red_segment.set_time_signatures([(3, 8), (4, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.dotted_sixteenths, count=1)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__set_rhythm_transform_keywords_03():
    '''Rhythm 'reverse' keyword.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.make_segment('red')
    red_segment.set_time_signatures([(3, 8), (4, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.dotted_sixteenths, reverse=True)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__set_rhythm_transform_keywords_04():
    '''Rhythm 'rotation' keyword.
    '''
    py.test.skip('implement eventually')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.make_segment('red')
    red_segment.set_time_signatures([(3, 8), (4, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.dotted_sixteenths, rotation=-1)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
