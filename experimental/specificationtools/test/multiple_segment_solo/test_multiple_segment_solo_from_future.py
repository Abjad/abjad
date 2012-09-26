from abjad import *
from experimental import *


def test_multiple_segment_solo_from_future_01():
    '''First segment defined after second.
    Absolute time signature request.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    blue_segment.set_divisions([(2, 16), (4, 16)])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    red_segment.set_time_signatures([(2, 8), (2, 8)])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_from_future_02():
    '''First segment defined after second.
    Time signature command request.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    red_segment.set_time_signatures(blue_segment.request_time_signature_command())

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_from_future_03():
    '''First segment defined after second.
    Time signature command request with request-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    blue_time_signatures = blue_segment.request_time_signature_command(reverse=True)
    red_segment.set_time_signatures(blue_time_signatures)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_from_future_04():
    '''First segment defined after second.
    Time signature command request with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    red_segment.set_time_signatures(blue_segment.request_time_signature_command(), reverse=True)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_from_future_05():
    '''First segment defined after second.
    Time signature command request with both request- and set-time reverse.
    Reverse indications effectively undo each other.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    blue_time_signatures = blue_segment.request_time_signature_command(reverse=True)
    red_segment.set_time_signatures(blue_time_signatures, reverse=True)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_from_future_06():
    '''First segment defined after second.
    Time signature material request.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    blue_segment.set_divisions([(2, 16), (4, 16)])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    red_segment.set_time_signatures(blue_segment.request_time_signatures())

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_from_future_07():
    '''First segment defined after second.
    Time signature material request with request-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    blue_time_signatures = blue_segment.request_time_signatures(reverse=True)
    red_segment.set_time_signatures(blue_time_signatures)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_from_future_08():
    '''First segment defined after second.
    Time signature material request with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    blue_time_signatures = blue_segment.request_time_signatures()
    red_segment.set_time_signatures(blue_time_signatures, reverse=True)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo_from_future_09():
    '''First segment defined after second.
    Time signature material request with both request- and set-time reverse.
    The reverse indications effectively undo each other.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)

    red_segment = score_specification.make_segment(name='red', index=0)
    blue_time_signatures = blue_segment.request_time_signatures(reverse=True)
    red_segment.set_time_signatures(blue_time_signatures, reverse=True)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
