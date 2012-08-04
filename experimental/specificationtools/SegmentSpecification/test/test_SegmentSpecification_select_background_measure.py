from abjad.tools import *
from experimental import *
from experimental.specificationtools import library
import py


def test_SegmentSpecification_select_background_measure_01():
    py.test.skip('working on this one now.')
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])
    last_measure = segment.select_background_measure(-1)
    segment.set_divisions_new([(2, 32)])
    segment.set_divisions_new([(3, 32)], timespan=last_measure)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert 
