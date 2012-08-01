from abjad.tools import *
from experimental import *
from experimental.specificationtools import library
import py


def test_single_segment_solo_boundary_cases_01():
    '''Second division setting overrides first division setting.
    '''
    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template) 
    segment = score_specification.append_segment('red') 
    segment.set_time_signatures([(4, 8), (3, 8)])
    segment.set_divisions([(3, 16)])
    segment.set_divisions([(1, 16)])
    segment.set_rhythm(library.thirty_seconds)

    score = score_specification.interpret()
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
