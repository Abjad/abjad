# -*- encoding: utf-8 -*-
import pytest
pytest.skip()
from abjad import *
import scoremanager


def test_BuildDirectoryManager__run_01():
    r'''Segment and material navigation work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)

    input_ = 'red~example~score u g q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles

    input_ = 'red~example~score u m q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles