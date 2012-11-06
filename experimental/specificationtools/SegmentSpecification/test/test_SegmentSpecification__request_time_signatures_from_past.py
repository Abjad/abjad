from abjad import *
from experimental import *


def test_SegmentSpecification__request_time_signatures_from_past_01():
    '''From-past time signature material request.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])  
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_time_signatures = red_segment.request_time_signatures()
    blue_segment.set_time_signatures(red_time_signatures)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_time_signatures_from_past_02():
    '''From-past time signature material request with smaller set-time count.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])  
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_time_signatures = red_segment.request_time_signatures()
    blue_segment.set_time_signatures(red_time_signatures, count=1)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_time_signatures_from_past_03():
    '''From-past time signature material request with larger set-time count.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])  
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_time_signatures = red_segment.request_time_signatures()
    blue_segment.set_time_signatures(red_time_signatures, count=5)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_time_signatures_from_past_04():
    '''From-past time signature material request with set-time index.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])  
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_time_signatures = red_segment.request_time_signatures()
    blue_segment.set_time_signatures(red_time_signatures, index=-1)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_time_signatures_from_past_05():
    '''From-past time signature material request with set-time index and count.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])  
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_time_signatures = red_segment.request_time_signatures()
    blue_segment.set_time_signatures(red_time_signatures, count=5, index=-1)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_time_signatures_from_past_06():
    '''From-past time signature material request with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])  
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_time_signatures = red_segment.request_time_signatures()
    blue_segment.set_time_signatures(red_time_signatures, reverse=True)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_time_signatures_from_past_07():
    '''From-past time signature material request with request-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])  
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_time_signatures = red_segment.request_time_signatures(reverse=True)
    blue_segment.set_time_signatures(red_time_signatures)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_time_signatures_from_past_08():
    '''From-past time signature material request with both request- and set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])  
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_time_signatures = red_segment.request_time_signatures(reverse=True)
    blue_segment.set_time_signatures(red_time_signatures, reverse=True)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
