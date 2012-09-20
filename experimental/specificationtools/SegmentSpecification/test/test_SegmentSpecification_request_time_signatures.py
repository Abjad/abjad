from abjad import *
from experimental import *


def test_SegmentSpecification_request_time_signatures_01():
    '''Trivial time signature request.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8)])  
    segment.set_divisions([(3, 16)])
    segment.set_rhythm(library.sixteenths)

    source = segment.request_time_signatures()
    segment = score_specification.make_segment(name='blue')
    segment.set_time_signatures(source)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_time_signatures_02():
    '''Time signature request counted to a small number.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8)])  
    segment.set_divisions([(3, 16)])
    segment.set_rhythm(library.sixteenths)

    source = segment.request_time_signatures()
    segment = score_specification.make_segment(name='blue')
    segment.set_time_signatures(source, count=1)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_time_signatures_03():
    '''Time signature request counted to a larger number.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8)])  
    segment.set_divisions([(3, 16)])
    segment.set_rhythm(library.sixteenths)

    source = segment.request_time_signatures()
    segment = score_specification.make_segment(name='blue')
    segment.set_time_signatures(source, count=5)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_time_signatures_04():
    '''Time signature request indexed without count.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8)])  
    segment.set_divisions([(3, 16)])
    segment.set_rhythm(library.sixteenths)

    source = segment.request_time_signatures()
    segment = score_specification.make_segment(name='blue')
    segment.set_time_signatures(source, index=-1)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_time_signatures_05():
    '''Time signature request indexed and counted.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8)])  
    segment.set_divisions([(3, 16)])
    segment.set_rhythm(library.sixteenths)

    source = segment.request_time_signatures()
    segment = score_specification.make_segment(name='blue')
    segment.set_time_signatures(source, count=5, index=-1)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_time_signatures_06():
    '''Time signature request reversed.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])  
    segment.set_divisions([(3, 16)])
    segment.set_rhythm(library.sixteenths)

    source = segment.request_time_signatures()
    segment = score_specification.make_segment(name='blue')
    segment.set_time_signatures(source, reverse=True)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
