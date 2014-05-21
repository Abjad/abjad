# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MakerFileWrangler_go_home_01():

    input_ = 'red~example~score k h q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker files',
        'Score manager - scores',
        ]
    assert score_manager._transcript.titles == titles


def test_MakerFileWrangler_go_home_02():

    input_ = 'k h q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - scores',
        'Score manager - maker files',
        'Score manager - scores',
        ]
    assert score_manager._transcript.titles == titles