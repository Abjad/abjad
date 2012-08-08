from abjad import *
from experimental import *
import py


def test_multiple_segment_solo_selector_boundary_cases_01():
    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    first_third_of_segment = segment.select_segment_ratio_part((1, 1, 1), 0)
    segment.set_divisions([(2, 16)])
    segment.set_divisions([(3, 16)], selector=first_third_of_segment)
    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.append_segment('blue')
    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    #helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
