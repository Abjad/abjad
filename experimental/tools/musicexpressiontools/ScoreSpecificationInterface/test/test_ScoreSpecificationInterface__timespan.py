from experimental import *


def test_ScoreSpecificationInterface__timespan_01():
    '''Score start-offset lookup.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    green_segment = score_specification.append_segment(name='green')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_rhythm(library.sixteenths, persist=False)
    blue_segment.set_rhythm(library.eighths, persist=False)
    lookup = score_specification.timespan.start_offset.look_up_rhythm_set_expression('Voice 1')
    green_segment.set_rhythm(lookup)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecificationInterface__timespan_02():
    '''Score start-offset lookup with translation.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    green_segment = score_specification.append_segment(name='green')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_rhythm(library.sixteenths, persist=False)
    blue_segment.set_rhythm(library.eighths, persist=False)
    offset = score_specification.timespan.start_offset.translate(Duration(6, 8))
    lookup = offset.look_up_rhythm_set_expression('Voice 1')
    green_segment.set_rhythm(lookup)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecificationInterface__timespan_03():
    '''Score stop-offset lookup with translation.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    green_segment = score_specification.append_segment(name='green')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    blue_segment.set_rhythm(library.eighths, persist=False)
    green_segment.set_rhythm(library.sixteenths, persist=False)
    offset = score_specification.timespan.stop_offset.translate(Duration(-1, 8))
    lookup = offset.look_up_rhythm_set_expression('Voice 1')
    red_segment.set_rhythm(lookup)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
