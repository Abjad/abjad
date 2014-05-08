# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_go_to_segments_01():
    r'''Goes from score segments to score segments.
    '''

    input_ = 'red~example~score g g q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles


def test_SegmentPackageWrangler_go_to_segments_02():
    r'''Goes from segment library to segment library.
    '''

    input_ = 'g g q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - segments',
        'Score manager - segments',
        ]
    assert score_manager._transcript.titles == titles