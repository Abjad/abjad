# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_BuildDirectoryManager__run_01():
    r'''Segment and material navigation work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)

    string = 'red~example~score u g q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build manager',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles

    string = 'red~example~score u m q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build manager',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles
