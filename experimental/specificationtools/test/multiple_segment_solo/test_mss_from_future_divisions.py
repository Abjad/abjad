from abjad import *
from experimental import *


def test_mss_from_future_divisions_01():
    '''From-future division command request.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_divisions([(3, 16), (4, 16)], contexts=['Voice 1'])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    blue_divisions = blue_segment.request_division_command('Voice 1')
    red_segment.set_divisions(blue_divisions)
    red_segment.set_rhythm(library.sixteenths)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_mss_from_future_divisions_02():
    '''From-future division command request with request-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_divisions([(3, 16), (4, 16)], contexts=['Voice 1'])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    blue_divisions = blue_segment.request_division_command('Voice 1', reverse=True)
    red_segment.set_divisions(blue_divisions)
    red_segment.set_rhythm(library.sixteenths)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_mss_from_future_divisions_03():
    '''From-future division command request with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_divisions([(3, 16), (4, 16)], contexts=['Voice 1'])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    blue_divisions = blue_segment.request_division_command('Voice 1')
    red_segment.set_divisions(blue_divisions, reverse=True)
    red_segment.set_rhythm(library.sixteenths)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_mss_from_future_divisions_04():
    '''From-future division command request with paired reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_divisions([(3, 16), (4, 16)], contexts=['Voice 1'])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    blue_divisions = blue_segment.request_division_command('Voice 1', reverse=True)
    red_segment.set_divisions(blue_divisions, reverse=True)
    red_segment.set_rhythm(library.sixteenths)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_mss_from_future_divisions_05():
    '''From-future division material request.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_divisions([(3, 16), (4, 16)], contexts=['Voice 1'])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    blue_divisions = blue_segment.request_divisions('Voice 1')
    red_segment.set_divisions(blue_divisions)
    red_segment.set_rhythm(library.sixteenths)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_mss_from_future_divisions_06():
    '''From-future division material request with request-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_divisions([(3, 16), (4, 16)], contexts=['Voice 1'])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    blue_divisions = blue_segment.request_divisions('Voice 1', reverse=True)
    red_segment.set_divisions(blue_divisions)
    red_segment.set_rhythm(library.sixteenths)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_mss_from_future_divisions_07():
    '''From-future division material request with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_divisions([(3, 16), (4, 16)], contexts=['Voice 1'])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    blue_divisions = blue_segment.request_divisions('Voice 1')
    red_segment.set_divisions(blue_divisions, reverse=True)
    red_segment.set_rhythm(library.sixteenths)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_mss_from_future_divisions_08():
    '''From-future division material request with paired reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    blue_segment.set_divisions([(3, 16), (4, 16)], contexts=['Voice 1'])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    blue_divisions = blue_segment.request_divisions('Voice 1', reverse=True)
    red_segment.set_divisions(blue_divisions, reverse=True)
    red_segment.set_rhythm(library.sixteenths)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
