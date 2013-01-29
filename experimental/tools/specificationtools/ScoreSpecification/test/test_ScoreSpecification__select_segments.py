from experimental.tools import *
import py


def test_ScoreSpecification__select_segments_01():
    '''The timespan-scoped single-context rhythm set expressions aren't coming out correctly.
    So the problem is relatively early in interpretation.
    '''
    py.test.skip('working on this one')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    green_segment = score_specification.append_segment(name='green')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_rhythm(library.sixteenths)
    segments = score_specification.select_segments('Voice 1')
    segments.timespan.set_rhythm(library.eighths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
