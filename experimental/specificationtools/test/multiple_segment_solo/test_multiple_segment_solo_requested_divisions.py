from abjad import *
from experimental import *
import py


def test_multiple_segment_solo_requested_divisions_01():
    '''Intersegment division material request.
    '''
    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(3, 8), (2, 8)])
    segment.set_divisions([(5, 16), (4, 16)])    
    segment.set_rhythm(library.sixteenths)
    red_divisions = segment.request_divisions(context_name='Voice 1')

    segment = score_specification.append_segment(name='blue')
    segment.set_time_signatures([(5, 8), (2, 8)])
    segment.set_divisions(red_divisions)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
