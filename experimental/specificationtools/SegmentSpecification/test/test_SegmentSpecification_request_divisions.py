from abjad import *
from experimental import *


def test_SegmentSpecification_request_divisions_01():
    '''Request all divisions from earlier segment. Reverse divisions.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    
    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(4, 16), (3, 16), (2, 16)])
    segment.set_rhythm(library.sixteenths)
    
    segment = score_specification.make_segment(name='blue')
    source = score_specification.request_divisions('Voice 1', 'red', segment_count=1)
    segment.set_divisions(source, reverse=True)

    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
