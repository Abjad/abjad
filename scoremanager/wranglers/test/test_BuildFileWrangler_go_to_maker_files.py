# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_go_to_maker_files_01():
    r'''From build directory to makers directory.
    '''

    input_ = 'red~example~score u k q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score Manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build files',
        'Red Example Score (2013) - maker files',
        ]
    assert score_manager._transcript.titles == titles