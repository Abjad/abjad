from abjad import *
from experimental import *


# TODO: Add rhythm request tests for requests between voices.

def test_SegmentSpecification_request_rhythm_from_past_01():
    '''Request rhythm from earlier segment.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_background_measure(0)
    right_measure = red_segment.select_background_measure(1)
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'], selector=right_measure)
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_voice_1_rhythm = red_segment.request_rhythm('Voice 1')
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_rhythm_from_past_02():
    '''Fit larger source rhythm into smaller target.
    '''    

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_background_measure(0)
    right_measure = red_segment.select_background_measure(1)
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'], selector=right_measure)
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(8, 8)])
    red_voice_1_rhythm = red_segment.request_rhythm('Voice 1')
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_rhythm_from_past_03():
    '''Reverse rhythm at request-time.
    '''    

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_background_measure(0)
    right_measure = red_segment.select_background_measure(1)
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'], selector=right_measure)
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_voice_1_rhythm = red_segment.request_rhythm('Voice 1', reverse=True)
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_rhythm_from_past_04():
    '''Reverse rhythm at set-time.
    '''    

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_background_measure(0)
    right_measure = red_segment.select_background_measure(1)
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'], selector=right_measure)
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_voice_1_rhythm = red_segment.request_rhythm('Voice 1')
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'], reverse=True)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_rhythm_from_past_05():
    '''Reverse rhythm at both request- and set-time.
    '''    

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_background_measure(0)
    right_measure = red_segment.select_background_measure(1)
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'], selector=right_measure)
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_voice_1_rhythm = red_segment.request_rhythm('Voice 1', reverse=True)
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'], reverse=True)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_rhythm_from_past_06():
    '''Rotate rhythm at request time.
    '''    

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_background_measure(0)
    right_measure = red_segment.select_background_measure(1)
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'], selector=right_measure)
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_voice_1_rhythm = red_segment.request_rhythm('Voice 1', rotation=8)
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_rhythm_from_past_07():
    '''Rotate rhythm at set time.
    '''    

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_background_measure(0)
    right_measure = red_segment.select_background_measure(1)
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'], selector=right_measure)
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_voice_1_rhythm = red_segment.request_rhythm('Voice 1')
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'], rotation=8)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_rhythm_from_past_08():
    '''Rhythm 'rotation' keyword set at both request- and set-time.

    The keywords undo each other with the addition of severed spanners.
    '''    

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_background_measure(0)
    right_measure = red_segment.select_background_measure(1)
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'], selector=right_measure)
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    red_voice_1_rhythm = red_segment.request_rhythm('Voice 1', rotation=8)
    blue_segment.set_rhythm(red_voice_1_rhythm, contexts=['Voice 1'], rotation=-8)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_rhythm_from_past_09():
    '''Request shorter rhythm and repeat to fill longer duration.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    left_measure = red_segment.select_background_measure(0)
    right_measure = red_segment.select_background_measure(1)
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'], selector=right_measure)
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(6, 8), (9, 8)])
    red_rhythm = red_segment.request_rhythm('Voice 1')
    blue_segment.set_rhythm(red_rhythm, contexts=['Voice 1'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
