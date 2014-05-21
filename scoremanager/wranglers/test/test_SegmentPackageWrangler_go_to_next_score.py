# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_go_to_next_score_01():

    input_ = 'red~example~score g >> q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Blue Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles


def test_SegmentPackageWrangler_go_to_next_score_02():

    input_ = 'g >> q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - scores',
        'Score manager - segments',
        'Blue Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles