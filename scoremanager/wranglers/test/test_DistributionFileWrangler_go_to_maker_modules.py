# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_go_to_maker_modules_01():
    r'''From distribution directory to makers directory.
    '''

    input_ = 'red~example~score d k q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution files',
        'Red Example Score (2013) - maker modules',
        ]
    assert score_manager._transcript.titles == titles