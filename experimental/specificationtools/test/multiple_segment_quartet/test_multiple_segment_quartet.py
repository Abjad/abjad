from abjad import *
from experimental import *
import py


def test_multiple_segment_quartet_01():
    '''Create 4-staff score S with sections T1, T2.
    Set T1 time signatures equal to [(3, 8), (3, 8), (2, 8), (2, 8)].
    Set T1 1 & 2 divisions equal to a repeating pattern of [(3, 16)].
    Set T1 1 & 2 rhythm equal to running 32nd notes.
    Set T1 3 & 4 divisions equal to T1 time signatures.
    Set T1 3 & 4 rhythm equal to note-filled tokens.

    Set T2 time signatures equal to the last 2 time signatures of T1.
    Let all other T1 specifications continue to T2.

    Tests for spanning divisions in 1 & 2 over T1 / T2.
    Tests for truncated divisions in 1 & 2 at the end of T2.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment(name='T1')
    segment.set_time_signatures([(3, 8), (3, 8), (2, 8), (2, 8)])

    upper = [segment.v1, segment.v2]
    segment.set_divisions([(3, 16)], contexts=upper)
    segment.set_rhythm(library.thirty_seconds, contexts=upper)

    lower = [segment.v3, segment.v4]
    segment.set_rhythm(library.note_filled_tokens, contexts=lower)

    segment = score_specification.append_segment(name='T2')
    source = score_specification['T1'].request_time_signatures()
    segment.set_time_signatures(source, index=-2, count=2)

    score = score_specification.interpret()

    assert score_specification['T1'].time_signatures == [(3, 8), (3, 8), (2, 8), (2, 8)]
    assert score_specification['T2'].time_signatures == [(2, 8), (2, 8)]

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_quartet_02():
    '''As above with different divisions.
    
    Tests for spanning divisions in 1 & 2 and also in 3 & 4.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment(name='T1')
    segment.set_time_signatures([(3, 8), (3, 8), (2, 8), (2, 8)])

    upper = [segment.v1, segment.v2]
    segment.set_divisions([(5, 16)], contexts=upper)
    segment.set_rhythm(library.thirty_seconds, contexts=upper)

    lower = [segment.v3, segment.v4]
    segment.set_divisions([(4, 16), (3, 16)], contexts=lower)
    segment.set_rhythm(library.note_filled_tokens, contexts=lower)

    segment = score_specification.append_segment(name='T2')
    source = score_specification['T1'].request_time_signatures()
    segment.set_time_signatures(source, index=-2, count=2)

    score = score_specification.interpret()

    assert score_specification['T1'].time_signatures == [(3, 8), (3, 8), (2, 8), (2, 8)]
    assert score_specification['T2'].time_signatures == [(2, 8), (2, 8)]

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_quartet_03():
    '''Render example [3]:
    Quartet in 2 segments. T1 time signatures 4/8 3/8. 
    F1 1:1 of measures then left part 3/16 and right part 5/16 divisions.
    F2 1:1 of meaures then [5/16, 3/16]
    F3 1:1 of total time then [3/16, 5/16] from F1.
    F4 1:1 of total time then [5/16, 3/16] from F2.
    Filled note tokens scorewide.
    T2 equal to T1 flipped about the y axis in all respects.
    ''' 
    py.test.skip('working on this one now.')
