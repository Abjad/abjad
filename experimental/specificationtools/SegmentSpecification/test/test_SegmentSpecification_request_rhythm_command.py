from abjad import *
from experimental import *
import py


def test_SegmentSpecification_request_rhythm_command_01():
    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(5, 16)])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    red_rhythm = red_segment.request_rhythm_command('Voice 1')
    blue_segment.set_rhythm(red_rhythm)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
