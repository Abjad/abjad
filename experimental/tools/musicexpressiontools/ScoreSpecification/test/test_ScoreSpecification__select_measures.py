from experimental import *


def test_ScoreSpecification__select_measures_01():
    '''Measure select expression dependent on segment select expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    green_segment = score_specification.append_segment(name='green')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    score_specification.set_rhythm(library.sixteenths)
    segments = score_specification.select_segments('Voice 1')[:2]
    most_measures = segments.timespan.select_measures('Voice 1')[1:-1]
    most_measures.timespan.set_rhythm(library.eighths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
