from abjad import *
from experimental import *
import py


def test_SegmentSpecification_request_divisions_from_future_01():

    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    blue_segment = score_specification.make_segment(name='blue')

    red_segment.set_time_signatures([(2, 8), (2, 8)])
    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    red_segment.set_rhythm(library.sixteenths)

    blue_divisions = blue_segment.request_divisions('Voice 1')
    red_segment.set_divisions(blue_divisions)
    blue_segment.set_divisions([(4, 16)])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
