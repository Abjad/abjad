# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_go_home_01():

    input_ = 'red~example~score g h q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score Manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Score Manager - scores',
        ]
    assert score_manager._transcript.titles == titles


def test_SegmentPackageWrangler_go_home_02():

    input_ = 'g h q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score Manager - scores',
        'Score Manager - segments',
        'Score Manager - scores',
        ]
    assert score_manager._transcript.titles == titles