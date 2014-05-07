# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_go_to_segments_01():
    r'''Goes from score build files to score segments.
    '''

    input_ = 'red~example~score u g q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build files',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles