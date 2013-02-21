from experimental import *


def test_SegmentSpecification__set_divisions_01():
    '''Set divisions from time signatures.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    time_signatures = red_segment.select_time_signatures('Voice 1')
    time_signatures = time_signatures.reflect()
    red_segment.set_divisions(time_signatures, contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
